# PageTwins results on Kaggle

| Model | Task | Input | Bases | Score | Defects found and named | Controls passed | Picks for A | Text-visible defects | Invalid |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | pairs | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.60 | 51% | 70% | 57% | 73% | 0 |
| claude-haiku-4-5-20251001 | pairs | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.46 | 36% | 55% | 38% | 41% | 0 |
| claude-haiku-4-5-20251001 | solo | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.45 | 45% | 90% clean pages unflagged |  | 64% | 0 |
| claude-haiku-4-5-20251001 | solo | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.37 | 37% | 90% clean pages unflagged |  | 46% | 0 |
| claude-sonnet-5-5-default | pairs | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.85 | 70% | 100% | 50% | 100% | 0 |
| claude-sonnet-5-5-default | pairs | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 1.00 | 100% | 100% | 50% | 100% | 0 |
| claude-sonnet-5-5-default | solo | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.63 | 63% | 100% clean pages unflagged |  | 90% | 0 |
| claude-sonnet-5-5-default | solo | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.98 | 98% | 100% clean pages unflagged |  | 97% | 0 |
| deepseek-r1-0528 | pairs | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.74 | 69% | 80% | 50% | 99% | 0 |
| deepseek-r1-0528 | solo | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.61 | 61% | 70% clean pages unflagged |  | 87% | 0 |
| gemini-3.5-flash-lite | pairs | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.80 | 60% | 100% | 53% | 86% | 0 |
| gemini-3.5-flash-lite | pairs | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.64 | 72% | 55% | 50% | 79% | 0 |
| gemini-3.5-flash-lite | solo | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.53 | 53% | 90% clean pages unflagged |  | 76% | 0 |
| gemini-3.5-flash-lite | solo | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.63 | 63% | 95% clean pages unflagged |  | 64% | 0 |
| gemini-3.7-flash | pairs | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.80 | 60% | 100% | 50% | 86% | 0 |
| gemini-3.7-flash | pairs | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.99 | 98% | 100% | 50% | 97% | 0 |
| gemini-3.7-flash | solo | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.56 | 56% | 100% clean pages unflagged |  | 80% | 0 |
| gemini-3.7-flash | solo | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.96 | 96% | 100% clean pages unflagged |  | 94% | 0 |
| gemma-4-31b-it | pairs | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.85 | 70% | 100% | 50% | 100% | 0 |
| gemma-4-31b-it | pairs | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.95 | 95% | 95% | 50% | 97% | 0 |
| gemma-4-31b-it | solo | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.67 | 67% | 95% clean pages unflagged |  | 96% | 0 |
| gemma-4-31b-it | solo | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.93 | 93% | 95% clean pages unflagged |  | 97% | 0 |
| glm-5 | pairs | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.85 | 70% | 100% | 50% | 100% | 0 |
| glm-5 | solo | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.53 | 53% | 80% clean pages unflagged |  | 76% | 2 |
| gpt-6-luna | pairs | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.84 | 68% | 100% | 51% | 97% | 0 |
| gpt-6-luna | pairs | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.96 | 93% | 100% | 50% | 90% | 0 |
| gpt-6-luna | solo | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.58 | 58% | 95% clean pages unflagged |  | 83% | 0 |
| gpt-6-luna | solo | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.89 | 89% | 100% clean pages unflagged |  | 84% | 0 |
| gpt-6.1-sol | pairs | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.85 | 70% | 100% | 50% | 100% | 0 |
| gpt-6.1-sol | pairs | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.98 | 96% | 100% | 50% | 94% | 0 |
| gpt-6.1-sol | solo | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.61 | 61% | 95% clean pages unflagged |  | 87% | 0 |
| gpt-6.1-sol | solo | vision | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.98 | 98% | 100% clean pages unflagged |  | 97% | 0 |
| qwen3-235b-a22b-instruct-2507 | pairs | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.69 | 52% | 85% | 47% | 74% | 2 |
| qwen3-235b-a22b-instruct-2507 | solo | text | B01,B02,B03,B04,B05,B06,B07,B08,B09,B10 | 0.37 | 37% | 100% clean pages unflagged |  | 53% | 1 |

## Per category (defects found and named in both orders for pairs; strict detection for solo)

| Model | Task | Input | missing_cta | hidden_price | contradiction | vague_headline | typos | placeholder_text | low_contrast | broken_image | blocking_popup | cut_off_text |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | pairs | text | 10/10 | 10/10 | 4/10 | 7/10 | 10/10 | 10/10 | 0/10 | 0/10 | 0/10 | 0/10 |
| claude-haiku-4-5-20251001 | pairs | vision | 6/10 | 5/10 | 0/10 | 2/10 | 2/10 | 4/10 | 3/10 | 2/10 | 10/10 | 2/10 |
| claude-haiku-4-5-20251001 | solo | text | 9/10 | 10/10 | 3/10 | 0/10 | 10/10 | 10/10 | 0/10 | 0/10 | 3/10 | 0/10 |
| claude-haiku-4-5-20251001 | solo | vision | 6/10 | 8/10 | 0/10 | 0/10 | 1/10 | 7/10 | 0/10 | 0/10 | 10/10 | 5/10 |
| claude-sonnet-5-5-default | pairs | text | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 0/10 | 0/10 | 10/10 | 0/10 |
| claude-sonnet-5-5-default | pairs | vision | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 |
| claude-sonnet-5-5-default | solo | text | 7/10 | 9/10 | 10/10 | 7/10 | 10/10 | 10/10 | 0/10 | 0/10 | 10/10 | 0/10 |
| claude-sonnet-5-5-default | solo | vision | 8/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 |
| deepseek-r1-0528 | pairs | text | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 0/10 | 0/10 | 9/10 | 0/10 |
| deepseek-r1-0528 | solo | text | 9/10 | 9/10 | 9/10 | 9/10 | 9/10 | 10/10 | 0/10 | 0/10 | 6/10 | 0/10 |
| gemini-3.5-flash-lite | pairs | text | 10/10 | 9/10 | 4/10 | 7/10 | 10/10 | 10/10 | 0/10 | 0/10 | 10/10 | 0/10 |
| gemini-3.5-flash-lite | pairs | vision | 10/10 | 8/10 | 2/10 | 7/10 | 10/10 | 8/10 | 0/10 | 10/10 | 10/10 | 7/10 |
| gemini-3.5-flash-lite | solo | text | 6/10 | 10/10 | 8/10 | 0/10 | 10/10 | 10/10 | 0/10 | 0/10 | 9/10 | 0/10 |
| gemini-3.5-flash-lite | solo | vision | 6/10 | 10/10 | 0/10 | 0/10 | 9/10 | 10/10 | 2/10 | 6/10 | 10/10 | 10/10 |
| gemini-3.7-flash | pairs | text | 10/10 | 9/10 | 10/10 | 10/10 | 10/10 | 10/10 | 0/10 | 0/10 | 1/10 | 0/10 |
| gemini-3.7-flash | pairs | vision | 10/10 | 9/10 | 9/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 |
| gemini-3.7-flash | solo | text | 7/10 | 9/10 | 10/10 | 10/10 | 10/10 | 10/10 | 0/10 | 0/10 | 0/10 | 0/10 |
| gemini-3.7-flash | solo | vision | 8/10 | 10/10 | 10/10 | 8/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 |
| gemma-4-31b-it | pairs | text | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 0/10 | 0/10 | 10/10 | 0/10 |
| gemma-4-31b-it | pairs | vision | 10/10 | 8/10 | 10/10 | 10/10 | 10/10 | 10/10 | 9/10 | 10/10 | 10/10 | 8/10 |
| gemma-4-31b-it | solo | text | 8/10 | 9/10 | 10/10 | 10/10 | 10/10 | 10/10 | 0/10 | 0/10 | 10/10 | 0/10 |
| gemma-4-31b-it | solo | vision | 9/10 | 10/10 | 10/10 | 9/10 | 10/10 | 10/10 | 7/10 | 10/10 | 10/10 | 8/10 |
| glm-5 | pairs | text | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 0/10 | 0/10 | 10/10 | 0/10 |
| glm-5 | solo | text | 9/10 | 9/10 | 9/10 | 2/10 | 10/10 | 10/10 | 0/10 | 0/10 | 4/10 | 0/10 |
| gpt-6-luna | pairs | text | 8/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 0/10 | 0/10 | 10/10 | 0/10 |
| gpt-6-luna | pairs | vision | 10/10 | 10/10 | 10/10 | 10/10 | 3/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 |
| gpt-6-luna | solo | text | 6/10 | 10/10 | 10/10 | 10/10 | 9/10 | 10/10 | 0/10 | 0/10 | 3/10 | 0/10 |
| gpt-6-luna | solo | vision | 8/10 | 9/10 | 9/10 | 10/10 | 3/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 |
| gpt-6.1-sol | pairs | text | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 0/10 | 0/10 | 10/10 | 0/10 |
| gpt-6.1-sol | pairs | vision | 10/10 | 10/10 | 10/10 | 10/10 | 6/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 |
| gpt-6.1-sol | solo | text | 7/10 | 9/10 | 10/10 | 10/10 | 10/10 | 10/10 | 0/10 | 0/10 | 5/10 | 0/10 |
| gpt-6.1-sol | solo | vision | 10/10 | 10/10 | 10/10 | 10/10 | 8/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 |
| qwen3-235b-a22b-instruct-2507 | pairs | text | 10/10 | 9/10 | 4/10 | 10/10 | 10/10 | 9/10 | 0/10 | 0/10 | 0/10 | 0/10 |
| qwen3-235b-a22b-instruct-2507 | solo | text | 7/10 | 10/10 | 1/10 | 0/10 | 10/10 | 9/10 | 0/10 | 0/10 | 0/10 | 0/10 |
