---
title: "Modeller Requirements for knowledge re-use"
author: "Alex Mikhalev"
date: 2021-03-07T10:02:39.396Z
lastmod: 2021-06-11T10:00:19+01:00

description: ""

subtitle: ""




aliases:
- "/modeller-requirements-for-knowledge-re-use-20e2e4ce12ea"

---

#### Context

Let’s have a small organisation running a “proper” strategic loop: OODA + PDCA

#### OODA

Observe Orient Decide Act — this loop is on the strategic level “surface” of the organisation, observing external trends: technology, market, global political trends, then orient organisation via artefacts like strategy.

#### PDCA

Plan Do Check Act — loop inside the organisation, pretty much extension of Act — once you decided to act you start your plan.

What I would like to have: the system or combination of collaborative systems, which allow retaining knowledge throughout the whole lifecycle and both loops — so the questions like “can we select this technology as part of (P)” can be answered with technologies from “Orient”, without re-doing the work: trend analysis, analysis of the technologies, market research.

At the same time, I would like to have all relevant information supporting actions on the “Act” step.

#### My opinion of existing MBSE and Knowledge Management tools

I looked at notion.so, coda.io, Jira/Confluence, Redmine, Asana, Spark Systems Architect, Rational Suite, Trello, Sci-Forma, Adato, you name it. I wasn’t able to find a perfect one and convince everyone to move into a single platform, hence my main concern is APIs and integration. Apart from model-based systems engineering, you normally need to have a tool for product management and tools for UX — Figma. Coda and notion allow performing product management, and knowledge management and to create actions + integrations with Figma and a number of other tools. Systems engineers praise [http://www.iquavis.com/](http://www.iquavis.com/) as a nearly perfect tool — and considering it came out of Japanese car manufacturers I tend to believe. Transition to something like iQuavis (or any other model-based systems engineering tools) is effort-consuming — they are not lightweight and require training (apart from installation), they also normally don’t care about my main concern — integration with other tools and assume (for their own benefit) you can force everyone to use single tool/single platform, but don’t accommodate other team members needs — coders will need code repository and wikis next to it and we will end up with multiple sources of truth. I prefer evolutionary approach and text (in Markdown) as ground truth: as long as we capture information in a single source in text form, I can build a design structure matrix (or QFD) view or tree visualisation out of the notion, it would not be as feature-complete as iQUAVIS, but it will allow having discussions and progress deliverables. Once we hit a limit of capability of notion with a large number of teams and people involved we can choose the right tool for the job from our build-up understanding of what we need — for example, [A-dato](https://www.a-dato.com/agile-scrum-kanban/) allows visualising project progress in fever chart (RAG), which allows seeing the status of the whole portfolio at the glance, without the need to enquire every team, which may be one of the key requirements for managing a large number of small projects.

* * *
Written on March 7, 2021 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/modeller-requirements-for-knowledge-re-use-20e2e4ce12ea)
