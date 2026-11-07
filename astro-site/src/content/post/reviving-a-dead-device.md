---
title: "Reviving a Dead Device: What an AI Agent Got Wrong Four Times"
subtitle: "A discontinued NAS with a 2019 bootloader, 1 GB of RAM and no display port — and four confident wrong diagnoses before the box finally booted."
slug: "reviving-a-dead-device"
description: "A dead NAS, a serial console that never enumerated, and a 2019 U-Boot that could not boot the image it shipped with. How an AI agent revived it — and the four wrong diagnoses that came first."
tags: ["ai-agents", "debugging", "embedded-linux", "infrastructure", "automation"]
author: "Dr Alexander Mikhalev"
date: "2026-11-06"
ogImage: "/img/cubbit-reviving-og.png"
draft: false
---

There is a class of work an agent cannot iterate on. No test suite, no CI, no rollback button, no second attempt unless a human resets the hardware. The device either boots or it does not.

This is that story. The useful part is not that the device booted.

A **Cubbit Cell**: a discontinued NAS-style appliance built on a Globalscale ESPRESSObin board. Marvell Armada 3720, two cores, 952 MB of RAM, 8 GB of eMMC, a 2 TB SATA disk, and a vendor bootloader from 2019 with no supported operating system left to boot. The goal was unremarkable — put a supported Linux on it and make it the next volume server in a SeaweedFS cluster that already had three nodes in production.

The first symptom was that there was no console. The board has no video output of any kind. The only serial path is a micro-USB port that is simultaneously the 5 V power inlet and a USB-to-UART bridge. Nothing enumerated. `ioreg` showed nothing. For a while the most reasonable hypothesis was a dead board, or a bridge chip someone had depopulated in production.

It was a charge-only cable.

## Three doors, in order

Getting a shell on this board meant opening three doors in the right order. Each one presented as exactly the same symptom — total silence — and each had a different cause.

**The cable.** A charge-only micro-USB cable produces no device node, no USB enumeration, and no error anywhere. That is indistinguishable from dead hardware. The bridge here turned out to be a Prolific PL2303, which we confirmed by USB identifier rather than by guessing at the board revision.

**The console.** With the right cable, we still could not use the obvious tools. macOS `cu` insists on creating a lock file in a root-owned directory and then reports the port as "Line in use" — an error that looks like a second process holding the device when no process does. macOS `screen` is from 2006 and has no `-Logfile`. The fix was to stop using terminal programs and open the tty directly with `termios`, which also had the useful property of surviving the device disappearing and reappearing.

**The bootloader.** This is where the vintage bit bites. The vendor's U-Boot is from 2018 and has no FIT support, so `bootm` rejected a perfectly valid flattened image with "Wrong Image Format". Armbian ships a FIT for this board. It cannot be booted by this bootloader. We hand-loaded the kernel, the initrd and the device tree with `booti` instead:

```
36239872 bytes read in 817 ms (42.3 MiB/s)     ← kernel  from mmc 1:3
18824641 bytes read in 424 ms (42.3 MiB/s)     ← initrd  from mmc 1:3
12046 bytes read in 20 ms (587.9 KiB/s)        ← dtb     from mmc 1:3
## Flattened Device Tree blob at 06f00000
Starting kernel ...
[    0.000000] Machine model: Globalscale Marvell ESPRESSOBin Board (eMMC)
[    0.000000] earlycon: ar3700_uart0 at MMIO 0x00000000d0012000 (options '115200n8')
[    4.430692] EXT4-fs (mmcblk0p3): mounted filesystem 37a0b904-bf87-47bf-874d-5e6dc940a1bd r/w
```

![The serial console capture of the working boot: U-Boot, three byte counts read from the eMMC, the kernel handover, and the root filesystem mounting from mmcblk0p3](/img/cubbit-console-boot-evidence.png)

*Verbatim serial capture. The whole chain, from reset to a login prompt: bootloader, three loads from the eMMC, kernel handover, root filesystem mounted, both services started.*

## The part worth reading

The box booted. Then, a few hours later, it went dark, and the agent handling it produced four wrong answers in a row. Each one was plausible. Each one was refuted by evidence that had already been collected.

> **"The eMMC install broke sshd."**
> The console log plainly recorded `Started ssh.service` at 08:02, from the eMMC — and the agent had SSHed into it successfully at 08:15. The claim was refuted by the very artefact the agent had been reading.

> **"`network-online.target` is blocking startup."**
> Also refuted by the same log, which recorded the wait service being *skipped*. On this system that target resolves in about thirteen seconds.

> **"The link never dropped."**
> Asserted from a serial console log. Except the serial console had been physically unplugged, so the log stopped at exactly the point where the claim required evidence. Absence of a log line is not evidence of the absence of an event.

> **"It's the connector."**
> This one turned out to be right, in the sense that the cable was faulty — but the kernel journal had been saying `check cabling!` for hours, and nobody had read it.

![The kernel journal from cubbit-cell showing the link downshifting to 100 Mbps and cycling every 25 seconds, with the fault becoming visible only when the cable was replaced](/img/cubbit-link-flap-timeline.png)

*The fault was in the kernel journal the entire time. Four identical "check cabling!" lines, and a link that only held for 25 seconds at a time.*

The failure mode is not stupidity. Every wrong answer was internally coherent, and every one of them would have been plausible to a human engineer working from the same incomplete view. The problem was that the agent reasoned *past the end of its evidence*, and stopped looking for the record that would break the story it had already told itself.

## What the fault actually was

The Ethernet cable was downgrading the link from 1 Gbps to 100 Mbps and cycling it roughly every 25 seconds. When carrier drops, `systemd-networkd` removes the static address from the interface. The host therefore stops answering ARP entirely and looks powered off — indistinguishable from a dead machine, and unfixable from a laptop over SSH.

There is a second-order failure here that cost more time than the cable itself. When the link came back, the machine was often *mid-boot*. The kernel resets every port until `sshd` binds, while mDNS is already up. So the signature was "everything refused except 5355" — which reads exactly like a broken SSH daemon, and nothing like a machine that had not finished starting yet.

![A diagnostic tree for the question "is the box dead?", showing the three checks that would have located the fault: is the MAC on the wire at all, is the link flapping, and are the obvious tools lying to you](/img/cubbit-diagnostic-tree.png)

*Every wrong diagnosis above came from skipping a box in the top row. The tree costs two minutes, and would have saved the day.*

One diagnostic detail is worth keeping whatever else you take from this: on that machine, unprivileged `arp -an` returns *nothing*, even for hosts that are plainly reachable and answering pings. `sudo arp -an` returns the truth. An agent that trusts the first result concludes the host is absent, and then reasons at length about a machine that is sitting right there.

## Where it ended up

The box now boots unattended from its own eMMC with no USB stick, no serial console and no human present, and comes up as a full member of a live cluster.

![The end state: Armbian 26.8.1 on the eMMC with an unattended boot, a 1.9 TB XFS store on the SATA disk with both tiers, a SeaweedFS volume server on port 8088 joining the existing master, and the design choices that made it survivable](/img/cubbit-final-stack.png)

*The end state. One device, five failed diagnoses, and a cluster that never noticed the difference.*

The cluster's other nodes run on Raspberry Pis with USB-attached storage, so the tier layout had to match: an untagged directory on the spinning disk and an `ssd`-tagged one, with the same weed build — `3.32`, byte-identical to the master — so the master treats the new node as one of its own.

| | |
|---|---|
| OS | Armbian 26.8.1 trixie, kernel `6.18.43-current-mvebu64` |
| Root | `/dev/mmcblk0p3` — eMMC, boots unattended with no USB stick |
| Store | 1.9 TB XFS (`LABEL=seaweed`) on the SATA disk, mounted at `/mnt` |
| Tiers | `/mnt/usbslow/weed` (default) + `/mnt/usbfast/weed/` (`ssd`), matching the rack |
| Storage | weed `3.32 758d70bd` — byte-identical build to the master |
| Role | volume server on `192.168.1.185:8088`, joining `rpi4node3:9333` |
| Rollback | eMMC **p2** still holds the vendor OS; the bootloader is in the SPI NOR |

A write-through test confirmed the end-to-end path: an object written through the filer landed as a volume on the new node and came back with an identical checksum.

Two design points came directly out of the outage, and both are worth more than the debugging.

**A data disk must never be able to wedge the operating system.** The store is mounted with `nofail` and a bounded device timeout. A disk that fails to appear now degrades the volume server; it does not take the box into emergency mode.

**A service that reconnects on its own must not depend on the network being up.** The volume server no longer waits for `network-online.target`. It retries the master every couple of seconds regardless, which is the behaviour it should have had from the start.

There is also a rollback path, which matters more than it sounds: the vendor's original operating system is still on a second partition of the same eMMC. The bootloader lives in the SPI NOR, so a bad write cannot brick the board, and the original system can be selected again by changing one environment variable.

## Five rules that came out of it

1. **Read the primary source, not the log you happen to have.** A serial console stops when the cable is unplugged. The kernel journal does not. Every one of the four wrong answers came from treating the end of a truncated log as the end of history.
2. **Check the boring explanations first.** A charge-only cable and a bad Ethernet cable cost more time than every interesting hypothesis combined. Neither appears in any documentation.
3. **Distinguish "the tool says" from "the thing is".** Unprivileged `arp` returning nothing is a fact about `arp`. It is not a fact about the host.
4. **Verify the running process, not the configuration file.** An edited unit file did not change the running process, because the daemon had not been told to re-read it. `/proc/<pid>/cmdline` settles this; grepping the file does not.
5. **Make the failure modes survivable, then go looking for the cause.** `nofail`, no network dependency, a second boot partition. These were added after the outage, and they are the reason the next outage is a five-minute event rather than a day.

## What to ask anyone who sends an agent at hardware

- **How does the agent establish ground truth when there is no CI?** Here it was `journalctl -b`, `/proc/<pid>/cmdline`, raw magic bytes, and `sudo arp -an`. If the answer is "it reads the logs", ask which logs, and whether they survive the thing being unplugged.
- **What stops the agent concluding "it is broken" from a partial read?** The failures above were all plausible stories that the evidence did not contradict, because the evidence had stopped.
- **What is the rollback?** For software, a branch. For a device, a second bootable partition and a bootloader outside the storage you are rewriting.
- **Can it make the system survive the failure it just diagnosed?** The `nofail` mount is worth more than the four hours of diagnosis that preceded it.

The device boots. The more durable result is the set of rules above, because every one of them is a rule about how an agent should behave when it is tired, blocked, and holding a story it wants to be true.
