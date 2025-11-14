# Add ChromaDB Crud operations

In the db folder, add the following CRUD operations that are specific to ChromaDB.

1. Write_Collection.  This function will take in the parameters collection_name, ID, textvalue, all of which are required, and an optional metadata
 1.1 The function will do a add operation, and be similiar to:
 collection.add(
    ids=["id1"],
    documents=["text"]
    metadatas=[{"chapter": 3, "verse": 16}]
)
where 'collection' will be the passed in collection_name (required), id1 will be the passed in ID value (required), text is the textvalue (required), and if metadata exists,
that will be inserted in the metadatas brackets.  Return a value of '1' if add was successful and using logger.debug,
add a message of "Successful Chroma add, with Collection name of ", collection_name, " and ID of ",ID.
If results failed, return a value of '-1' and using logger.critical, add a message of "Add FAILED to ChromaDB for collection", collection_name, "and ID of "ID
2. Update_Collection.  This function will take in the parameters collection_name, ID, textvalue, all of which are required, and an optional metadata
2.1 The function will do a update operation and be similiar to:
collection.update(
    ids=["id1"],
    documents=["doc1"],
    metadatas=[{"chapter": 3, "verse": 16}]

)
where 'collection' will be the passed in collection_name, id1 will be the passed in ID value, text is the textvalue, and if metadata exists,
that will be inserted in the metadatas bracket.  Return a value of '1' if add was successful and using logger.debug,
add a message of "Successful Chroma Update, with Collection name of ", collection_name, " and ID of ",ID.
If results failed, return a value of '-1' and using logger.critical, add a message of "Update FAILED to ChromaDB for collection", collection_name, "and ID of "ID
3. Delete_Collection.  This function will take in the parameters collection_name, and ID value, both of which are required.
3.1 The function will do a delete operation and be similiar to:
collection.update(
    ids=["id1"],

)
where 'collection' will be the passed in collection_name, id1 will be the passed in ID value.  Return a value of '1' if add was successful and using logger.debug,
add a message of "Successful Chroma Delete, with Collection name of ", collection_name, " and ID of ",ID.
If results failed, return a value of '-1' and using logger.critical, add a message of "Delete FAILED to ChromaDB for collection", collection_name, "and ID of "ID
4. Query_Collection.  This function will take in the parameters collection_name, and query_text, both of which are required.
A optional parameter num_results, of type integer, will have a default value of 25
4.1 The function will do a delete operation and be similiar to:
results = collection.query(
    query_text=["query_text"]
    n_results = num_results

)
where 'collection' will be the passed in collection_name, query_text will be the passed in query_text value.
Chroma returns .query and .get results in columnar form. You will get a results object containing lists of ids, embeddings, documents, and metadatas of the records that matched your .query or get requests. Embeddings are returned as 2D-numpy arrays.

class QueryResult(TypedDict):
    ids: List[IDs]
    embeddings: Optional[List[Embeddings]],
    documents: Optional[List[List[Document]]]
    metadatas: Optional[List[List[Metadata]]]
    distances: Optional[List[List[float]]]
    included: Include

class GetResult(TypedDict):
    ids: List[ID]
    embeddings: Optional[Embeddings],
    documents: Optional[List[Document]],
    metadatas: Optional[List[Metadata]]
    included: Include
.query results also contain a list of distances. These are the distances of each of the results from your input queries. .query results are also indexed by each of your input queries. For example, `results["ids"][0]` contains the list of records IDs for the results of the first input query.

If command is successful, using logger.debug, add a message of "Successful Chroma Query, with Collection name of ", collection_name, " and query_text of ",query_text.
If results failed, return a value of '-1' and using logger.critical, add a message of "Query FAILED to ChromaDB for collection", collection_name, "and query_text of ", query_text
