import os
import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load and validate environment variables
load_dotenv()

uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME", "shortener_db")

if not uri:
    raise ValueError("MONGO_URI environment variable is required")
if not db_name:
    raise ValueError("DB_NAME environment variable is required")

# Configuration for link ID generation; Default to Machine ID 1 if not set in .env
machine_id_str = os.getenv("MACHINE_ID", "1")
try:
    MACHINE_ID = int(machine_id_str)
except ValueError:
    raise ValueError(f"MACHINE_ID must be an integer, got: {machine_id_str}")

# Shift of 20 bits allows ~1 million sequence numbers per machine before rolling over
# (Machine ID takes the upper bits, Sequence takes the lower 20 bits)
MACHINE_OFFSET = 20 

# Connect and verify connection to MongoDB
client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("✅ Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"❌ Connection failed: {e}")

# Define Database and Collections
db = client[db_name]
url_collection = db["urls"]
counters_collection = db["counters"]

# Create shortUrl index
try:
    url_collection.create_index("shortUrl", unique=True)
except Exception as e:
    print(f"Index creation warning: {e}")

# Generator Function
def get_next_sequence_id(sequence_name: str = "url_id"):
    """
    Atomically increments a counter and combines it with Machine ID.
    Formula: (MACHINE_ID << MACHINE_OFFSET) | <seq_num>
    """
    # Get the next sequence number from the 'counters' collection
    counter = counters_collection.find_one_and_update(
        {"_id": sequence_name},          # Look for the counter named "url_id"
        {"$inc": {"sequence_value": 1}}, # Increment by 1
        upsert=True,                     # Create if it doesn't exist
        return_document=True             # Return the NEW value
    )
    
    seq_num = counter["sequence_value"]
    
    # id = Machine ID OR Sequence Number
    unique_id = (MACHINE_ID << MACHINE_OFFSET) | seq_num
    
    return unique_id