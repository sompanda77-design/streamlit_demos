import streamlit as st
import json
from openai import OpenAI

def display():
    OPENAI_API_KEY = st.session_state.OPENAI_API_KEY
    MODEL_NAME = st.session_state.MODEL_NAME

    outer_cols = st.columns([3,1])    

    with outer_cols[0]:
        st.header("OpenAI API - Randomness Parameters")
        st.markdown("""
            <style>
            .column {
                height: 500px;
                overflow-y: auto;
            }
            </style>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)


        with col1:
            st.markdown('''
                        <h4 style="color:blue">temperature</h4>
                What sampling temperature to use. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
            ''',  unsafe_allow_html=True)

        with col2:
            st.markdown('''
                        <h4 style="color:blue">top_p</h4>
                An alternative to sampling with temperature, using nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
            ''',  unsafe_allow_html=True)

    with outer_cols[1]:
        st.video("https://youtu.be/zasTo1SAYIw")


    st.markdown('<hr>', unsafe_allow_html=True)
    col1, col2 = st.columns(2) 

    with col1:
        SYSTEM_MESSAGE = st.text_input("Enter the system message", help="Provide general context and instructions for the AI" ,value="You are a helpful assistant")
        USER_MESSAGE = st.text_input("Enter the user message", help="Ask a question or provide a prompt for the AI to respond to",value="Give me 5 names best suited for AI models")

        st.markdown('<hr>', unsafe_allow_html=True)
        INCLUDE_ONLY = st.radio("Include", ["temperature", "top_p"], help="Choose either temperature or top_p")

    with col2:
        MAX_TOKENS = st.slider("max_tokens: ", value=200, min_value=1, max_value=2048, step=1, help="The maximum number of tokens to generate a response")
        N = st.slider("n: number of response choices", value=1, min_value=1, max_value=10, step=1, help="How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep n as 1 to minimize costs.")    
        if INCLUDE_ONLY == "temperature":
            TEMPARATURE_1 = st.slider("temperature 1", value=0.2, min_value=0.0, max_value=2.0, step=0.1, help="What sampling temperature to use.Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.")
            TEMPARATURE_2 = st.slider("temperature 2", value=1.6, min_value=0.0, max_value=2.0, step=0.1, help="What sampling temperature to use.Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.")            
 
        else:
            TOP_P_1 = st.slider("top_p 1", value=0.2, min_value=0.0, max_value=1.0, step=0.1, help="An alternative to sampling with temperature, using nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.")
            TOP_P_2 = st.slider("top_p 2", value=0.8, min_value=0.0, max_value=1.0, step=0.1, help="An alternative to sampling with temperature, using nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.")            
    MESSAGES = [{"role": "system", "content": SYSTEM_MESSAGE}, {"role": "user", "content": USER_MESSAGE}]


    st.markdown('<hr>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with  col1:

        with st.container():
            st.code(f"MODEL_NAME: {MODEL_NAME}\nMAX_TOKENS: {MAX_TOKENS}\nN: {N}")  
            if INCLUDE_ONLY == "temperature":
                st.code(f"TEMPERATURE: {TEMPARATURE_1} / {TEMPARATURE_2}")
            else:
                st.code(f"TOP_P: {TOP_P_1} / {TOP_P_2}")


        if INCLUDE_ONLY == "temperature":
            st.code(
                '''
                        from openai import OpenAI

                    client = OpenAI(api_key=OPENAI_API_KEY)

                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=MESSAGES,
                        max_tokens=MAX_TOKENS,
                        n=N,
                        temperature=TEMPARATURE,
                    )
            '''
            )
        else:
            st.code(
                '''
                        from openai import OpenAI

                    client = OpenAI(api_key=OPENAI_API_KEY)

                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=MESSAGES,
                        max_tokens=MAX_TOKENS,
                        n=N,
                        top_p=TOP_P,
                    )
                '''
            )

    with col2:
        st.caption("Messages")
        st.write(MESSAGES)

    st.markdown('<hr>', unsafe_allow_html=True)
    client = OpenAI(api_key=OPENAI_API_KEY)

    if st.button("Submit"):

        def get_response(temp_or_top_p):

            if INCLUDE_ONLY == "temperature":
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=MESSAGES,
                    max_tokens=MAX_TOKENS,
                    n=N,
                    temperature=temp_or_top_p,
                )
            else:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=MESSAGES,
                    max_tokens=MAX_TOKENS,
                    n=N,
                    top_p=temp_or_top_p,
                )
            if INCLUDE_ONLY == "temperature":
                expander_text = f"Response with temperature {temp_or_top_p}"
            else:
                expander_text = f"Response with top_p {temp_or_top_p}"
            
            with st.expander(expander_text):
                response_dict = response.to_dict() 
                response_json = json.dumps(response_dict, indent=2)
                st.json(response_json)

            finish_reasons = []
            for index, choice in enumerate(response.choices):
                with st.chat_message("assistant"):
                    st.write(choice.message.content)
                finish_reasons.append(choice.finish_reason)

            st.code(f"System Fingerprint: {response.system_fingerprint}" )

        col1, col2 = st.columns(2)

        with col1:
            if INCLUDE_ONLY == "temperature":
                get_response(TEMPARATURE_1)
            else:
                get_response(TOP_P_1)

        with col2:
            if INCLUDE_ONLY == "temperature":
                get_response(TEMPARATURE_2)
            else:
                get_response(TOP_P_2)

# Voice Narration of the Page
'''
Hello there!
Here, we will discuss the two key parameters that affect the randomness of the AI's response.

Lets head on to our website and select the chapter 'Randomness affecting Parameters' and plug in the API key.
So, what is randomness? Well, it is the variation in the AI's response. In other words, it is the difference in the AI's response when you submit the same prompt multiple times.

The first parameter is temperature. It is a value between 0 and 2. 
A higher value like 1 will make the output more random, while a lower value like 0.2 will make it more focused and deterministic. 
In other words, our AI will be more creative with higher temperature and more deterministic with lower temperature.

The second parameter is top_p. It is an alternative to sampling with temperature, using nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
It is a value between 0 and 1. A higher value like 1 will make the output more random, while a lower value like 0.1 will make it more focused and deterministic.

OpenAI suggests using either temperature or top_p, but not both at the same time.

Let's see how these parameters affect the AI's response.

First, lets enter the system message and user message. You know about these messages from the previous chapters. This time, lets ask the AI to give us 5 names best suited for AI models.

Next, let us keep the max_tokens as 200 and n as 1. 

You can see the sliders for temperature and top_p where you can set the values.

This page allows us to try 2 different values for temperature and see responses for both side by side.

We will set the temperature to the same value, say 0.2 in both the inputs.

See the code where the temperature parameter is added along with other already discussed parameters. The values passed on the parameters are here and see that the temperature parameter is set to 0.2 for both the inputs. Also, note the messages array.

Now, lets submit the request and wait for the response.

We can see that the 2 responses are generated. But, aren't they very close?

Now, let's set the temperature of the second input to 1.0 and see how the AI's response changes.

Can you see the difference? This time the AI's response is more random and creative. What do you think? 
So, we understand that the higher the temperature, the more random and creative the AI's response is.

You can also see the response JSON here in this block. Just click to expand and you can see the response object.

Its time to try the top_p parameter. Lets go back up and select top_p and set it to the same value, say 0.2 in both the inputs.

Values are updated in the code. See that instead of temperature, top_p is used. Lets submit!

The same way as see have seen in the temperature , the responses are very similar but not the same. 
Its because the AI considers the results of the tokens with top_p probability mass.

Now, let's set the top_p of the second input to a higher value, say 1.2 and see how the AI's response changes.

This time the AI's response is more random and creative. You can see it from the choice of words used in the second try.

Play around with these parameters and see how they affect the response generated by the AI model.

Lets meet in the next section. Good Bye!

'''        