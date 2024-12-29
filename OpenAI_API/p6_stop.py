import streamlit as st
import json
from openai import OpenAI
def display():
    OPENAI_API_KEY = st.session_state.OPENAI_API_KEY
    MODEL_NAME = st.session_state.MODEL_NAME
    outer_cols = st.columns([3,1])
    with outer_cols[0]:
        st.header("OpenAI API - Stop Parameter")
        st.markdown('''
                        <h4 style="color:blue">stop</h4>
                        Stop sequence is a string or list of strings. The API will stop generating further tokens when it encounters the stop sequence.
                        Up to 4 sequences can be provided.\n
                        A single string: <code>stop: "end"</code> \n
                        Multiple strings: <code>stop: ["at", "today"]</code>
                        ''', unsafe_allow_html=True)

    with outer_cols[1]:
        st.video("https://youtu.be/YrxMJvwA3XM")

    st.markdown('<hr>', unsafe_allow_html=True)
    col1, col2, col3= st.columns(3) 
    
    with col1:
        SYSTEM_MESSAGE = st.text_input("Enter the system message", help="Provide general context and instructions for the AI" ,value="You are a helpful assistant")
        USER_MESSAGE = st.text_input("Enter the user message", help="Ask a question or provide a prompt for the AI to respond to",value="Write a short story about a robot")


    with col2:
        MAX_TOKENS = st.slider("max_tokens: ", value=200, min_value=1, max_value=2048, step=1, help="The maximum number of tokens to generate a response")


    with col3:
        STOP_1 = st.text_input("stop 1",placeholder="any word or phrase")
        STOP_2 = st.text_input("stop 2",placeholder="any word or phrase")
        STOP_3 = st.text_input("stop 3",placeholder="any word or phrase")
        STOP_4 = st.text_input("stop 4",placeholder="any word or phrase")

        STOP = []
        if STOP_1:
            STOP.append(STOP_1)
        if STOP_2:
            STOP.append(STOP_2)
        if STOP_3:
            STOP.append(STOP_3)
        if STOP_4:
            STOP.append(STOP_4)

    MESSAGES = [{"role": "system", "content": SYSTEM_MESSAGE}, {"role": "user", "content": USER_MESSAGE}]



    st.markdown('<hr>', unsafe_allow_html=True)
    col1, col2 = st.columns([3,2])
    with  col1:
        st.code(f"MODEL_NAME: {MODEL_NAME} \nMAX_TOKENS: {MAX_TOKENS} \nSTOP: {STOP}")
        st.code(
            '''
                    from openai import OpenAI

                client = OpenAI(api_key=OPENAI_API_KEY)

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=MESSAGES,
                    max_tokens=MAX_TOKENS,
                    stop=STOP
                )
        '''
        )

    with col2:
        st.caption("Messages")
        st.write(MESSAGES)
    st.markdown('<hr>', unsafe_allow_html=True)
    if st.button("Submit"):

        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=MESSAGES,
            max_tokens=MAX_TOKENS,
            stop=STOP
        )

        response_dict = response.to_dict() 
        response_json = json.dumps(response_dict, indent=2)
        response_text = response.choices[0].message.content
        col1, col2 = st.columns(2)
        with col1:
            st.write(response_text)
        with col2:
            st.json(response_json)

# Voice Narration of the Page
'''
Hi there!
Welcome Back. In this section, we will discuss the stop parameter.

Head over to our website and select the chapter 'Stop Parameter'.

This parameter is essential for controlling when your AI-generated text should end.

Here's how it works: When the AI generates text and encounters the stop sequence you’ve defined, it will immediately cease its output. This gives you precise control over the length and structure of the responses.
You can specify up to four stop sequences.It can be a single string or multiple strings.

Lets see this in action.

We have our usual system and let's ask the AI to write a short story about a robot.
The max tokens is set to 200 and lets leave it as it is.

Now, we have to define the stop sequence. lets say we want the AI to stop generating text when it encounters the word "end".

Click on the submit button to see the AI response. We can also see the response object here.
The story has stopped at some point. But it is not because of the stop sequence. It is because the max tokens is set to 200.
We can see that the finish reason is "length". So in this case, the stop sequence word "end" was not generated in the response.

Now, lets try a different stop sequence.
This time, lets make it the symbol ".". Now, when the AI encounters the symbol ".", it will stop generating text.

Click on the submit button to see the AI response. 
The story has stopped at some point. This time it is because of the stop sequence. We can see that the finish reason is "stop".
So in this case, the stop sequence "." was generated in the response.

Let's try adding another stop sequence. We will add another symbol ",".

Click on the submit button to see the AI response. 
Now we see that the story has stopped even earlier. This is because the stop sequence "," was generated in the response.    

You can experiment with different stop sequences to see how it affects the AI response.

Try it out and have fun!
'''