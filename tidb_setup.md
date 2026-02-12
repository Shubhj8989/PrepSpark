# How to Set Up TiDB Cloud for PrepSpark ☁️

TiDB Cloud is a free, MySQL-compatible database perfect for hosting your Streamlit app's data.

## Step 1: Create a Free Account
1.  Go to [TiDB Cloud Sign Up](https://tidbcloud.com/).
2.  Sign up with Google or GitHub (it's fastest).
3.  Click **"Create Cluster"**.
4.  Select **"Serverless"** (It's free forever!).
5.  Region: Choose one closest to you (e.g., AWS us-east-1).
6.  Click **"Create"**. (It takes ~30 seconds).

## Step 2: Get Connection Details
1.  Once the cluster is ready, click **"Connect"** (top right).
2.  Select **"Connect with formatted text"**.
3.  You will see values for `Host`, `Port`, `User`, `Password`.
    *   *Note: Click "Generate Password" if needed.*
4.  **COPY these values**. You will need them for Streamlit Secrets.

## Step 3: Initialize the Database (Create Tables)
Your database starts empty. You need to create the tables.
1.  In TiDB Cloud console, go to **"SQL Editor"** (left sidebar).
2.  Start a new query.
3.  Copy the content of `init_db.sql` from your project files (I've simplified this for you).
4.  Paste it into the SQL Editor and click **"Run"**.
    *   *This creates the `users` and `study_sessions` tables.*

## Step 4: Add Secrets to Streamlit Cloud
1.  Go to your app on [Streamlit Cloud](https://share.streamlit.io/).
2.  Click **Manage App** (bottom right) -> **Settings** (⋮) -> **Secrets**.
3.  Paste the following (fill in your TiDB details):

```toml
[secrets]
DB_HOST = "gateway01.us-east-1.prod.aws.tidbcloud.com" 
DB_USER = "your-tidb-user.root"
DB_PASSWORD = "your-generated-password"
DB_NAME = "test"
DB_PORT = 4000
# Note: TiDB default DB name is usually 'test', check your connection details.
```
*Note: Make sure `DB_PORT` is 4000 (standard for TiDB), though our app defaults to it.*

## Step 5: Reboot App
Once secrets are saved, Streamlit will automatically restart your app. It should now connect successfully! 🚀
