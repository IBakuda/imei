from dotenv import load_dotenv
import os

load_dotenv()


# API_TOKEN = 'sijRhanpYvrleWdVCTvNT4TzCeXy9URBMfxa4aPa802bc4a3'
API_TOKEN = 'e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b'

SERVICE_ID = 12

WHITE_LIST = [385980042]

BOT_TOKEN = os.getenv('BOT_TOKEN')

URL_CHECK: str = "https://api.imeicheck.net/v1/checks"


# model_config = SettingsConfigDict(
#     env_file=join(dirname(__file__), '.env'),
#     env_file_encoding='utf-8'
# )