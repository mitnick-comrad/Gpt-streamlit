##### Pakages needed ########
#pip install langchin
#pip install openai
#pip install faiss-cpu
# pip install tiktoken
##### Use #######
# How to use: from Chatbot import model
# model('question here') ###Basic
# model('query',similarity_range,no_of_search_results_for_answer)  #######similarity_range 0 to 1 and number_of_search_results_for_answer is intiger less than 10 as recommended limit ########### For Custom use
##### Code #####
import time
context=[]
def model(question,y=0.43,io=5,uk=16):

    import os
    ko=[]
    if y>1:
        y=0.43
    
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    OpenAI_KEY='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' #client GPT4 Key
    embeddings = OpenAIEmbeddings(openai_api_key=OpenAI_KEY)
    def chunky(tex):
        s=''
        for a in tex:
            s+=a[0].page_content
            s+='\n'
            if len(s)>50000:
                break
        return s
    dr= [hp for hp in range(117)]
    import random
    random.shuffle(dr)
    for a in dr[:58]:

        if os.path.exists(f'/content/drive/MyDrive/model/faiss_index_datamodel_{a}'):
            retriever= FAISS.load_local(f'/content/drive/MyDrive/model/faiss_index_datamodel_{a}',embeddings)
            k= retriever.similarity_search_with_score(question,k=5)
            z=[h[1] for h in k]
            if min(z)<y:
                ko.extend(k)
            if len(ko)>uk:
                break
    ko.sort(key= lambda g: g[1])
    #print(len(ko),' ',ko[0][1])

    #print(ko[:10])

    #print(ko[0][1])
    prompt= f""" '''{chunky(ko[:io])}'''
    Reffering only to above infromation answer the question from the auther's perspective as a casual and friendly essay type response in simple words with examples if any from the information above along with self-caring, and explain everything in detail.

    ''' {question}''' """
    import os
    from openai import OpenAI
    client = OpenAI(

        api_key='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',
    )
    try:
        message=[{
                    "role": "system",
                    "content": "You are an Assistant that answer questions from the author's perspective who is 'Thich Nhat Hanh' with empathy, emotional wellbeing and advice on how to self-reflect as per question, based on the given user information and conditions to the user questions with respect to the context provided."
                        }]
        message.extend(context)
        message.append({
                    "role": "user",
                    "content": prompt,

                })
        response = client.chat.completions.create(
            messages=message,
            
            model="gpt-3.5-turbo-0125",
        )
        context.append({'role':'user', 'content': question})
        context.append({'role':'assistant', 'content': response.choices[0].message.content})
        if len(context)>10:
            context= context[2:]
            
        '''op=''
        for chunk in response:
            op+=chunk.choices[0].delta.content or '''''
        return response.choices[0].message.content
    except Exception as e:
        #return e
        return "Can't answer that might be technical error or the question is not answerable due to certain development guidelines."

#start= time.time()
print(model('What is the path to peace?',uk=50))
#stop= time.time()
#print('Runtime is : ',stop - start)