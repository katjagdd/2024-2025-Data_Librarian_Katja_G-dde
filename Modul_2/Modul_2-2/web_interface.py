{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "7f2c6692-4caa-4db1-8e95-662d45d9f9df",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Java started and loaded: pyterrier.java, pyterrier.terrier.java [version=5.11 (build: craig.macdonald 2025-01-13 21:29), helper_version=0.0.8]\n",
      "2025-01-23 12:07:02.805 WARNING streamlit.runtime.state.session_state_proxy: Session state does not function when running a script without `streamlit run`\n",
      "2025-01-23 12:07:03.604 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run /home/katja/anaconda3/lib/python3.12/site-packages/ipykernel_launcher.py [ARGUMENTS]\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "False"
      ]
     },
     "execution_count": 1,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#learn more about streamlit: https://docs.streamlit.io/\n",
    "\n",
    "import streamlit as st\n",
    "import pyterrier as pt\n",
    "import pickle\n",
    "import os\n",
    "\n",
    "if not pt.java.started():\n",
    "    pt.java.init()\n",
    "\n",
    "INDEX_PATH = os.getcwd() + \"/cc_index_mult/data.properties\"\n",
    "DATA_PATH =  os.getcwd() + \"/cc_index_mult/cc_publications.pkl\"\n",
    "\n",
    "def init():\n",
    "    index = pt.IndexFactory.of(INDEX_PATH)\n",
    "    st.session_state[\"engine\"] = pt.terrier.Retriever(index, wmodel=\"TF_IDF\")\n",
    "    st.session_state[\"data\"] = pickle.load(open(DATA_PATH, \"rb\"))\n",
    "\n",
    "def search(query):\n",
    "\n",
    "    res = st.session_state[\"engine\"].search(query)\n",
    "    fields_to_show = ['text', 'tags', 'url', 'author', 'description']\n",
    "\n",
    "    for _, row in res.iterrows():\n",
    "\n",
    "       \n",
    "        score = round(row['score'], 2)\n",
    "\n",
    "        sel_entry = st.session_state[\"data\"][st.session_state[\"data\"]['docno'] == row['docno']]\n",
    "        if sel_entry.empty:\n",
    "            continue \n",
    "        entry = sel_entry.iloc[0]\n",
    "\n",
    "        for field in fields_to_show:\n",
    "            if field == \"text\":\n",
    "                st.title(entry[field])\n",
    "            else:\n",
    "                st.write(f\"{field.capitalize()}: \\t {entry[field]}\")\n",
    "\n",
    "        st.write(f\"Score: {score}\")\n",
    "        st.divider()\n",
    "\n",
    "\n",
    "if not \"engine\" in st.session_state:\n",
    "    init()\n",
    "\n",
    "query = st.sidebar.text_input(\"Query\")\n",
    "st.sidebar.button(\"Search\", on_click=search, args=(query,))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5a88a526-a93b-4d67-87c8-b6e58840e8ea",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
