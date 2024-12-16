import streamlit as st
import json

def display():
    OPENAI_API_KEY = st.session_state.OPENAI_API_KEY
    MODEL_NAME = st.session_state.MODEL_NAME

    outer_cols = st.columns([3,1])

    with outer_cols[0]:    
        st.header("OpenAI API - Cost affecting Parameters")
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
                        <h4 style="color:blue">max_tokens</h4>
                        The maximum number of tokens to generate a response. The higher the value, the longer the response will be.
                        ''', unsafe_allow_html=True)

        with col2:
            st.markdown('''
                        <h4 style="color:blue">n</h4>
                        The number of response choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep n as 1 to minimize costs.
                        ''',  unsafe_allow_html=True)

    with outer_cols[1]:
        st.video("https://youtu.be/qx_8lK9Quzo")

    col1, col2 = st.columns(2)
    with col1:
        SYSTEM_MESSAGE = st.text_input("Enter the system message", help="Provide general context and instructions for the AI" ,value="You are a funny friend")
        USER_MESSAGE = st.text_input("Enter the user message", help="Ask a question or provide a prompt for the AI to respond to",value="Tell me a random joke")

    with col2:
        MAX_TOKENS = st.slider("max_tokens: ", value=200, min_value=1, max_value=2048, step=1, help="The maximum number of tokens to generate a response")
        N = st.slider("n: number of response choices", value=1, min_value=1, max_value=10, step=1, help="How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep n as 1 to minimize costs.")
    MESSAGES = [{"role": "system", "content": SYSTEM_MESSAGE}, {"role": "user", "content": USER_MESSAGE}]


    st.markdown('<hr>', unsafe_allow_html=True)
    col1, col2= st.columns(2)
    with  col1:
        st.code(f"MODEL_NAME: {MODEL_NAME}\nMAX_TOKENS: {MAX_TOKENS}\nN: {N}")
        st.code(
            '''
                    from openai import OpenAI

                client = OpenAI(api_key=OPENAI_API_KEY)

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=MESSAGES,
                    max_tokens=MAX_TOKENS,
                    n=N,
                )
        '''
        )


    with col2:
        st.caption("Messages")
        st.write(MESSAGES)
    st.markdown('<hr>', unsafe_allow_html=True)
    if st.button("Submit"):



        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=MESSAGES,
            max_tokens=MAX_TOKENS,
            n=N,
        )

        st.subheader("Response:")

        response_dict = response.to_dict() 
        response_json = json.dumps(response_dict, indent=2)
        st.json(response_json)

        with st.container(border=True):
            choice_cols = st.columns(len(response.choices))
            for index, choice in enumerate(response.choices):
                with choice_cols[index]:
                    st.subheader(f"Choice {index + 1}")
                    st.code(f"response.choices[{index}].message.content")
                    with st.chat_message("assistant"):
                        st.write(choice.message.content)                    
                    st.caption(f"Finish Reason: {choice.finish_reason}")


        with st.container(border=True):
            token_cols = st.columns(3)
            with token_cols[0]:
                st.caption("response.usage.prompt_tokens")
                st.metric("Prompt Tokens", response.usage.prompt_tokens)
            with token_cols[1]:
                st.caption("response.usage.completion_tokens")
                st.metric("Completion Tokens", response.usage.completion_tokens)
            with token_cols[2]:
                st.caption("response.usage.total_tokens")
                st.metric("Total Tokens", response.usage.total_tokens)


# Voice Narration - another version

'''
Hi There! Welcome back. We will see about 2 important parameters that affects the token usage and thereby affects the cost.

Lets head on to our website and select the chapter 'Cost affecting Parameters' and plug in the API key.
The first parameter is max_tokens. This parameter specifies the maximum number of tokens to generate a response. The higher the value, the longer the response will be. The more tokens you generate, the more it will cost you. So, keep that in mind.

The second parameter is n. This parameter specifies the number of response choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep n as 1 to minimize costs. 

This time, lets ask our AI to tell us a joke.
Now, lets try the 'n' parameter first. I am changing the value from 1 to 2.

In the code, you can see that max tokens and n are added. 
Max tokens is set to 200 and n is set to 2. So, we should get 2 jokes!

And, lets submit the request and see the response.

We can see that there are 2 choices now and there are 2 jokes!
The token usage for completion tokens has doubled as well because it generated 2 responses. Hope you get the point.

Now, lets try the max_tokens parameter. Let's go back to the top.
Set the n to 1 and set the max_tokens to 100.
This time lets ask it to provide a long story which will surely exceed 100 tokens.

See the new values to be sent in the request.

Lets submit the request and see the output.

The response is generated but it stops at some point. This is because the AI has reached the maximum token limit.
The finish reasons tell us why the AI stopped generating the response.
In our last example, the finish reason was 'stop' but now it is 'length'. This is because the max_tokens is set to 100 and the story is longer than that.

Taking a closer look at the token usage, we can see the number of tokens used for the completion same as the max_tokens we have set.

Try playing around with these parameters and see how they affect the response generated by the AI model.
Good Luck!
'''

