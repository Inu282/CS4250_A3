#-------------------------------------------------------------------------
# AUTHOR: Alvin Le
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #3
# TIME SPENT: ~3 Days
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# importing some Python libraries
from pymongo import MongoClient, errors
from datetime import datetime

def connectDataBase():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        return client['A4_DB']
        
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        return None

def createDocument(col, docId, docText, docTitle, docDate, docCat):
    term_dict = {}
    docText = docText.lower()
    terms = docText.split(" ")

    for term in terms:
        term = term.strip(",.!?")  
        term_dict[term] = term_dict.get(term, 0) + 1

    term_objects = [{"term_text": term, "num_chars": len(term), "term_count": count} for term, count in term_dict.items()]

    doc = {
        "_id": int(docId), 
        "text": docText,
        "title": docTitle,
        "num_chars": len(docText.replace(" ", "")),  
        "date": datetime.strptime(docDate, "%Y-%m-%d"),
        "category": docCat,
        "terms": term_objects
    }

    col.insert_one(doc)

def deleteDocument(col, docId):
    col.delete_one({"_id": int(docId)})  

def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    deleteDocument(col, docId) 
    createDocument(col, docId, docText, docTitle, docDate, docCat)  

def getIndex(col):
    index = {}
    for doc in col.find():
        title = doc['title']
        for term_obj in doc['terms']:
            term = term_obj['term_text']
            entry = f"{title}:{term_obj['term_count']}"

            if term in index:
                index[term].append(entry)
            else:
                index[term] = [entry]

    for term in index:
        index[term].sort()  
        index[term] = ', '.join(index[term])

    return dict(sorted(index.items()))
