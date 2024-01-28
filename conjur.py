
import requests
import os
import base64

# Function to authenticate with Conjur and retrieve an access token
def conjur_authenticate():
    conjur_authn_url = "http://localhost:8080/authn/myConjurAccount/frank@db/authenticate"
    api_key = "<FRANK API TOKEN>"  # Host's API Key

    response = requests.post(conjur_authn_url, data=api_key, verify=False)
    if response.status_code != 200:
        raise Exception("Authentication failed")

    encoded_token = base64.b64encode(response.content).decode('utf-8')
    return encoded_token

# Function to retrieve a secret from Conjur
def retrieve_secret(variable_id, access_token):
    conjur_variable_url = f"http://localhost:8080/secrets/myConjurAccount/variable/{variable_id}"
    headers = {"Authorization": f"Token token=\"{access_token}\""}

    response = requests.get(conjur_variable_url, headers=headers, verify=False)
    if response.status_code != 200:
        raise Exception("Failed to retrieve secret")

    return response.text

# Main function to connect to PostgreSQL and execute a query
def main():
    access_token = conjur_authenticate()
    
    db_username = retrieve_secret("db/POSTGRES_HOST_AUTH_METHOD", access_token)
    db_password = retrieve_secret("db/POSTGRES_HOST_AUTH_METHOD", access_token)
    db_name = retrieve_secret("db/POSTGRES_PASSWORD", access_token)

    print(db_username, db_password,db_name)

    # conn_string = f"host='localhost' dbname='{db_name}' user='{db_username}' password='{db_password}'"
    
    # # Connect to your postgres DB
    # conn = psycopg2.connect(conn_string)
    
    # # Execute a query
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM example_table")

    # # Fetch and print the result
    # for row in cursor.fetchall():
    #     print(row)  # Assuming 'row' is a tuple of column values

    # # Close the cursor and connection
    # cursor.close()
    # conn.close()

if __name__ == "__main__":
    main()
