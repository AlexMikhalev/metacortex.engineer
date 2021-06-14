Cloud computing security, common questions and my answers
#########################################################
:date: 2010-01-15 23:58
:author: Alex
:tags: cloud, general, web

I have a several friends, who have a great product ideas, based on
complex scientific algorithms. Each time when I suggest using cloud
computing for developing product we go through a round of questions. I
will put them down here, so I can reference it.

If you want to make online product in 2010, your solution should be
scalable. It should be able to handle 10 users as well as 10000, one
million. One of the ways to achieve it for startup is to leverage cloud
computing architecture. Other way is to raise a lot of money and put
your servers in secure datacenter under nuclear station in Switzerland.

Cloud computing is insecure if you compare it with switch off computer
with hard drive locked in the safe. Compared to other solutions it is
comparably secure and security risks can be mitigated.

\*Q: If we deploy it on somebody else infrastructure, we basically gave
them away code with a lot of work behind.\*

A: This statement is only partially correct. Yes, member of the staff
will theoretically be able to access running virtual appliance from host
server, yes, he theoretically can dump memory, then retrieve encryption
keys and then debug your code into working algorithm. But, if you
application so "interesting", I bet you already have very secure storage
- switched off computer and secure safe in some vault (and you work in
finance, MOD HQ, MI5 or MI6 etc.), because if you are not, you are
making this up and everything else you are doing potentially less secure
then submitting job in the cloud.

\*Q: Well, in this sense my home server is more secure in then the
cloud.\*

A: When defending some data against malicious access, the only question
matter "How much it costs?" see [this comic](http://xkcd.com/538/
"Security") for a simple example. It is race about how much you are
ready to spend and how much your competitor will spend in order to get
your data. Depending on security of your house, it may cost hundred of
pounds/dollars to get your server (physically). Compare it to hacking
into amazon cloud architecture or bribing their sysadmin (which one? in
what zone?). I bet odds are not in favour of the home server. I am
really against home server as home server doesn't have scalability and
have a high latency, which will be crucial for your users.

\*Q: Well, if my home server will be stolen, there will be a trace like
physical intrusion and then insurance can pay the damage.\*

A: Patent your algorithm or application. Provisional patent will cost
around 250 pounds (100$ for US) and will protect you for a year. This
have a big advantage as you can talk about your application loudly,
which may attract investors.

Amazon Elastic cloud pros:

1. Strong firewall by default. Instance is not automatically visible to
outside would. You have to configure firewall in order to be able to
login to your own box.

2. Instance can be started only using X509 certificates or logging in
using [MFA](http://aws.amazon.com/security/#5 "MFA"). MFA is a
convenient standard way for online protection (my bank uses it).

3. Proper designed backend servers are invisible to outside world and
can be located anywhere (eu or us), making attack difficult.

4. You can scale up and DOWN, which is very important for startup
(leverage).

5. Traffic between nodes can be encrypted using products like VPN Cubed.

I believe if you are paranoid about your application, you can encrypt
some part of the virtual machine which contains protected application
(cryptfs etc.), and then setup key server with rotating keys which will
be used to decrypt "especially secret" part of the code during runtime.
Of cause all configuration is secure as long as your key distribution
server is secure (somewhere in Switzerland, under nuclear station, you
know the drill), thus I think patenting is a better option. The bottom
line is that you have product and your customers, or you don't.

Great application, sitting on switched off computer with hard drive
doesn't make any money. Cloud computing is a very cheap way to create
great scalable architecture and compared to alternatives - home server,
co-location, your own laptop, is no less secure.
