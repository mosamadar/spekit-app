import enum

@enum.unique
class MessageResponse(enum.Enum):
    FOLDER_CREATED = "Folder created successfully."
    FOLDER_CREATION_ERROR = "Folder could not be created."

    DOCUMENT_CREATED = "Document created successfully."
    DOCUMENT_CREATION_ERROR = "Document could not be created."

    TOPIC_CREATED = "Topic created successfully."
    TOPIC_CREATION_ERROR = "Topic could not be created."

    DOCUMENTS_FOUND = "Your desired documents have been found successfully."
    MISSING_PARAMS = "You are either missing topic name or folder name."



def get_available_documents(documents):
    if documents:
        return set(map(lambda x:x["document"], documents))
    else:
        return []