import streamlit as st
from openai import OpenAI
import json
import pandas as pd
def display():
    OPENAI_API_KEY = st.session_state.OPENAI_API_KEY
    MODEL_NAME = st.session_state.MODEL_NAME
    st.header("OpenAI API - Streaming")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('''
                    <h4 style="color:blue">stream</h4>
                    The OpenAI API allows you to stream the response as it is generated.\n 
                    This is useful when you want to display the response as it is generated, rather than waiting for the entire response to be generated before displaying it. \n
                    <code>stream: True</code>
                    ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
                    <h4 style="color:blue">stream_options</h4>
                    Only set when stream is true. \n
                    Use this option to include the usage field in the response. The usage field provides information about the number of tokens used in the response. \n
                    <code>include_usage: True</code>
                    ''', unsafe_allow_html=True)    

    st.markdown('<hr>', unsafe_allow_html=True)
    col1, col2, col3= st.columns(3) 
    
    with col1:
        SYSTEM_MESSAGE = st.text_input("Enter the system message", help="Provide general context and instructions for the AI" ,value="You are a helpful assistant")
        USER_MESSAGE = st.text_input("Enter the user message", help="Ask a question or provide a prompt for the AI to respond to",value="Write a short poem about Robots")


    with col2:
        MAX_TOKENS = st.slider("max_tokens: ", value=200, min_value=1, max_value=2048, step=1, help="The maximum number of tokens to generate a response")


    with col3:
        STREAM = st.checkbox("stream", value=True, help="Set to true to stream the response as it is generated")
        INCLUDE_USAGE = st.checkbox("include_usage", value=False, help="Set to true to include the usage field in the response")




    MESSAGES = [{"role": "system", "content": SYSTEM_MESSAGE}, {"role": "user", "content": USER_MESSAGE}]


    st.markdown('<hr>', unsafe_allow_html=True)
    col1, col2 = st.columns([3,2])

    with  col1:
        st.code(f"MODEL_NAME: {MODEL_NAME} \n MAX_TOKENS: {MAX_TOKENS} \n STREAM: {STREAM} \n INCLUDE_USAGE: {INCLUDE_USAGE}")
        st.code(
            '''
                    from openai import OpenAI

                client = OpenAI(api_key=OPENAI_API_KEY)

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=MESSAGES,
                    max_tokens=MAX_TOKENS,
                    stream=STREAM,
                    stream_options={"include_usage": INCLUDE_USAGE}
                )
        '''
        )

        st.write('Response is streamed as chunks of data. You can access the token text and the entire chat response as shown below:')
        st.code('''
        chat_response = ''
        for chunk in response:
            token_text = chunk.choices[0].delta.content
            print(token_text) // print the token text
            chat_response += token_text   
        print(chat_response) // print the entire chat response                            
        ''')
  

    with col2:
        st.caption("Messages")
        st.write(MESSAGES)
    st.markdown('<hr>', unsafe_allow_html=True)
    ai_response = ''

    if st.button("Submit"):
    
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=MESSAGES,
            max_tokens=MAX_TOKENS,
            stream=STREAM,
            stream_options={"include_usage": INCLUDE_USAGE},
        )

        with st.chat_message("assistant"):
            response_container = st.empty()

        ai_response = ''
        json_list = []
        response_text_list = []
        # Stream the response
        for chunk in response:

            response_dict = chunk.to_dict() 
            response_json = json.dumps(response_dict, indent=2)
            json_list.append(response_json)
            if len(chunk.choices) > 0:
                response_text_list.append(chunk.choices[0].delta.content)   
            else:
                response_text_list.append(None)
            # Check if the chunk has choices and delta content
            if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                    if chunk.choices[0].delta.content is not None:
                        token_text = chunk.choices[0].delta.content
                        ai_response += token_text

                        response_container.write(ai_response)
                        

        response_df = pd.DataFrame({'response_json': json_list, 'response_text': response_text_list})
        
        col1, col2, col3 = st.columns([1,2,2])
        with col1:
            with st.container(border=True):
                st.info("Response Chunks")
                st.dataframe(response_df[['response_text']])
        with col2:
            with st.container(border=True):
                st.info("First Chunk")
                # first record json 
                st.json(response_df.iloc[0]['response_json'])
        with col3:
            with st.container(border=True):
                st.info("Last Chunk")
                # last record json 
                st.json(response_df.iloc[-1]['response_json'])



# Voice Narration of the Page
'''
Hi there!
Welcome Back. In this section, we will discuss the streaming parameter.

Let's go to our website and select the chapter 'Streaming'.
Remember to plug in your OpenAI API key and select the model.
In this lesson, as usual, we will be using gpt-4o-mini.

To have a better user experience, It is very important to start displaying the response as soon as possible, instead of waiting for the entire response to be generated.

Streaming helps us to stream the response as it is generated. 

Stream is a boolean parameter, and it is set to False by default.
We need to set it to True to stream the response.

Unlike the normal response, the streaming response is not a single string, but a list of chunks.
Each chunk contains a token text of the response. 
We need to gather all the token texts to get the entire response.

Since the response comes in chunks, by default, the other output parameters like usage, finish_reason, etc. are not included in the chunks.

To get this information, it comes with another parameter called stream_options. In stream_options, we can have another parameter called include_usage.

Setting include_usage to True will include the token usage information in the last chunk of the response.

Now, let's see this in action.

We will set the system message to "You are a helpful assistant" and the user message to "Write a short poem about Robots".

Max tokens is set to 200.
Notice the option to set stream and include_usage.
First, let's try to set stream to True and include_usage to False.

See that the parameter values reflect our selection including the the message list, which will be used to generate the response.

Here is the code to generate the response.

As mentioned earlier, the response is not a single string, but a list of chunks.
To read the response chunks, we need to iterate through the response chunks.
for each chunk, chunk.choices[0].delta.content will give us the token text of the response.
We need to gather all the content in a variable called chat_response and finally print the entire chat response.

Now, lets Click on the submit button to see the response being streamed.
We got a nice little poem about robots.

Now, let's break down the response.
The first table here shows all the chunks and the corresponding token text.
The second table here shows the first chunk and the third one shows the last chunk.

In the first chunk, see the delta content which is the first token generated.
The last chunk has a blank delta. 
We don't see the usage information anywhere here.

Now, let's set stream to True and include_usage to True.

See that the parameter values reflect our selection including the the message list.

Now, let's click on the submit button.

We got the response streamed as chunks.

Notice that the last chunk now has the usage information.
The rest of the response format is the same as before.

This is how you can stream the response as it is generated and also get the usage information.

That's all for this lesson.

Thank you for watching.

'''
