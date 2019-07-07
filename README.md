# xizhi
Xizhi is the actor server in the HWAT backend. Its responsibility is to wait for job from message queue and analyse handwriting features. Xizhi's name is inspired by the great Chinese writer in Jin Dynasty, Wang Xizhi(303-361)



To Qiushi,

* About the Client Model
    *   Instance has two functionality:
        1. register: input <image list> output: <user_model, status, msg>
        2. authentication:  input <image, user_model> output: <status, msg>

I have given sample code to use the module.
And if you have any question about the code, plz feel free to knock me on WeChat.

Oh I have changed the version of some packages, plz update them using requirements.txt in both xizhi/ and Hand.../

* The folder setup is like this:
    - xizhi/
        - Handwriting-Authentication-System/
            - ... all auth module codes ... `<you can clone github directly>`
        - server.py
        - ... other stuffs in repo `xizhi`.

Fangrui 7th, Jul