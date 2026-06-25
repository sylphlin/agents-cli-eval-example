# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

import os
import google.auth

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


SIMPLE_PROMPT = """你是一個對聯創作機器人。請根據用戶的要求寫出一副對聯。"""

DETAILED_PROMPT = """你是一個精通傳統文學與對聯格律的「對聯創作機器人」。
收到出題規範（題目、字數限制、嵌字體格）時，請嚴格遵守以下創作鐵律：
1. **字數絕對精準（首要硬性條件）**：
   - 題目若要求 N 字對聯，上聯與下聯的漢字數必須各自精準等於 N 個漢字！（標點符號不計入，絕對切勿多寫或少寫任何一字）
   - 例如要求5字聯，上聯與下聯都必須剛好是5個字；要求7字聯，上聯與下聯都必須剛好是7個字。
2. **嵌字格律落點精準控制**：
   - 鶴頂格（冠頭格）：指定二字分別為「上聯第1字」與「下聯第1字」。
   - 雁足格（藏尾格）：指定二字分別為「上聯最後一字」與「下聯最後一字」。
   - 腹嵌格：指定二字分別位於上下聯的正中央字位。
   - 魁鬥格：上聯第1字嵌第一個字，下聯最後一字嵌第二個字。
   - 連理格：指定二字相鄰連續出現在語句中。
   - 碎錦格：指定多字全數出現在上下聯中。
3. **對仗工整雅致**：詞性相對、意境喜慶優雅。
4. **輸出格式**：請明確清晰標示：
上聯：[剛好N個漢字]
下聯：[剛好N個漢字]"""

model_name = os.environ.get("COUPLET_MODEL_NAME", "gemini-3.5-flash")
thinking_level = os.environ.get("COUPLET_THINKING_LEVEL", "medium")
prompt_mode = os.environ.get("COUPLET_PROMPT_MODE", "detailed")

# Allow direct custom instruction override from environment
custom_instruction = os.environ.get("COUPLET_SYSTEM_INSTRUCTION")
if custom_instruction:
    selected_instruction = custom_instruction
else:
    selected_instruction = DETAILED_PROMPT if prompt_mode.lower() == "detailed" else SIMPLE_PROMPT


root_agent = Agent(
    name="couplet_generator",
    model=Gemini(
        model=model_name,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    generate_content_config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level=thinking_level.lower(),
        ),
    ),
    instruction=selected_instruction,
    tools=[],
)

app = App(
    root_agent=root_agent,
    name="app",
)
