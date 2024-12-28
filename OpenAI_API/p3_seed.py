import streamlit as st
from openai import OpenAI
import json
def display():
    OPENAI_API_KEY = st.session_state.OPENAI_API_KEY
    MODEL_NAME = st.session_state.MODEL_NAME

    outer_cols = st.columns([3,1])
    with outer_cols[0]:
        st.header("OpenAI API - Seed parameter")
        st.markdown('''
                    <h4 style="color:blue">seed</h4>
                    This feature is in Beta. If specified, openai will make a best effort to sample deterministically, such that repeated requests with the same <span style="color:blue">seed</span> and parameters should return the same result. Determinism is not guaranteed, and you should refer to the <span style="color:blue">system_fingerprint</span> response parameter to monitor changes in the backend.
                    ''',unsafe_allow_html=True)
    with outer_cols[1]:
        st.video("https://youtu.be/YrxMJvwA3XM")

    st.markdown('<hr>', unsafe_allow_html=True)
    col1, col2 = st.columns(2) 

    with col1:
        SYSTEM_MESSAGE = st.text_input("Enter the system message", help="Provide general context and instructions for the AI" ,value="You are a helpful assistant", )
        USER_MESSAGE = st.text_input("Enter the user message", help="Ask a question or provide a prompt for the AI to respond to",value="Give me 10 Random names")


    with col2:
        MAX_TOKENS = st.slider("max_tokens: ", value=200, min_value=1, max_value=2048, step=1, help="The maximum number of tokens to generate a response")
        col1, col2 = st.columns(2)
        with col1:
            SEED_1 = st.number_input("seed 1", value=25, help="A random seed to use for the chat completion. If you set the seed, you will get the same result each time you run the code with the same seed value.")
        with col2:
            SEED_2 = st.number_input("seed 2", value=25, help="A random seed to use for the chat completion. If you set the seed, you will get the same result each time you run the code with the same seed value.")
    MESSAGES = [{"role": "system", "content": SYSTEM_MESSAGE}, {"role": "user", "content": USER_MESSAGE}]


    st.markdown('<hr>', unsafe_allow_html=True)
    col1, col2= st.columns(2)
    with  col1:
        
        with st.container():
            st.code(f"MODEL_NAME: {MODEL_NAME}\nMAX_TOKENS: {MAX_TOKENS}\nSEED: {SEED_1} / {SEED_2}")
            st.code(
                '''
                        from openai import OpenAI

                client = OpenAI(api_key=OPENAI_API_KEY)

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=MESSAGES,
                    max_tokens=MAX_TOKENS,
                    seed=SEED
                )
        '''
        )

    with col2:

        st.caption("Messages")
        st.write(MESSAGES)
    st.markdown('<hr>', unsafe_allow_html=True)
    if st.button("Submit"):



        

        client = OpenAI(api_key=OPENAI_API_KEY)

        def get_response(seed):

            with st.spinner("Waiting for the response..."):
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=MESSAGES,
                    max_tokens=MAX_TOKENS,
                    seed=seed
                )

            st.code(f"System Fingerprint: {response.system_fingerprint}")

            st.subheader("AI message:")

            finish_reasons = []
            for index, choice in enumerate(response.choices):
                st.caption(f'Message on index {index} is :',)
                with st.chat_message("assistant"):
                    st.write(choice.message.content)
                finish_reasons.append(choice.finish_reason)


            st.subheader("Response:")
            response_dict = response.to_dict() 
            response_json = json.dumps(response_dict, indent=2)
            st.json(response_json)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"With Seed {SEED_1}" )
            get_response(SEED_1)

        with col2:
            st.subheader(f"With Seed {SEED_2}")
            get_response(SEED_2)

# Voice Narration of the Page
'''
Hello!

For many of our use cases, we want to ensure that the response is deterministic. 
OpenAI provides the deterministic response by using the seed parameter. 
Lets headover to our website and click on the chapter 'consistancy parameter'.
Remember to set the OPENAI_API_KEY and MODEL_NAME in the sidebar.
Seed is a random number that we can pass along with the request.
If specified, the system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result.
This is achieved by using the same backend for the same seed.
To verify that the same backend is used, OpenAI API has added a response parameter called system_fingerprint.
If the system_fingerprint is same for two requests, it means that the same backend was used to generate the response, and the response will likely be same.
But, the determinism is not guaranteed, and the response may vary for the same seed.

Let's see how it works.

This time, we will ask the AI to give us 10 Random names.

We will make two requests with same seed and see if the response is same or not.
We expect that the system_fingerprint will be same for both the requests, and the response will be same. 
Let's see if it is true.

Note that the code now has the seed parameter along with the other regular parameters we have been using.
The message array carries the system message and the user message.

Lets submit the request and wait for the response.

Okay, we got the response. First, let's check the system fingerprint.
We can see that the system fingerprint is same for both the requests.
This means that the same backend was used to generate the response, and the response will likely be same.

Now, let's check the response. Its mostly same, but not exactly.
This is because the response is not guaranteed to be same for the same seed.
It is just a best effort to make the response deterministic for the same seed.

Now, let's change one of the seed to say, 90000. This should return different responses as the seed is different.

This time, the system fingerprint is different, which means that the response is generated from different backend.
The response is also different, as expected.

That's all for the seed parameter.
Lets meet in the next one.
Good Bye!


'''