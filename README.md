# LLaMA_editor_GUI

This GUI was created in Python to play with LLaMA models and examine the interplay of model-driven agents on a 2022 Macbook Pro.  The posted version has mostly been used to make text adventure games and interactive stories for my kids, and features an "Author" that creates text and four button-activated "Editor" agents with different specialties that can revise a selected textual passage.

***image***

## Installation and performance:

To run the model, first install llama_cpp_python (abetlen/llama-cpp-python), then download a quantized LLaMA model (here's a large repository: https://huggingface.co/TheBloke) and enter the model path in the line that reads "llm = Llama(model_path="***your selected model here***", n_ctx=4096)"

The "QUEUE TEXT FOR AGENTS" section of the code can be edited to repurpose the editors -- for example, as metacognitive narrators or characters in a role playing game.

One for the "q4" quantized 13B LLaMA2 models, one should see ~10 tokens/s in normal use on an Apple M2 Max processor. Output quality will degrade as the number of tokens 

## Sample output:

Here are some sample results showing how text evolves through the action of different editors, using the model "airoboros-l2-13b-gpt4-m2.0.Q4_K_M.gguf":

1. Initial generated text: 

"In a world not too far from now, lived a teenage girl named Elysia. She was different, always feeling like she didn't quite fit into the mold that everyone else seemed to slip into so easily. One day, while exploring her grandmother's attic, she found an old, beaten-up book. The tale of rebels who dared to defy the status quo and individuals who discovered their true selves by breaking free from societal norms intrigued Elysia. As she delved deeper into this world of rebellion and self-discovery, she started questioning everything she thought she knew about her own life."

2. "Cut back" editor's output:

"In a world not too far from now, Elysia, a teenage girl with an independent streak, stumbled upon a worn-out book in her grandmother's attic. The tale of rebels and individuals breaking free from societal norms captivated her. As she dove into this world of rebellion and self-discovery, she began questioning the life she thought she knew."

3. "Descriptive" editor's output (given passage #2):

"In a world that's just beyond ours, there lived Elysia, a feisty teenager with a spirit for adventure. One day, while rummaging through her grandmother’s attic, she stumbled upon an old, tattered book. Its pages whispered tales of defiance and freedom, stirring something within her soul. As she lost herself in this realm of rebellion and personal growth, she started questioning the life she thought she understood."

3. "Excitement" editor's output (given passage #3):

"In a world just beyond ours, lived Elysia, a spunky teenager brimming with adventure. One afternoon, while exploring her grandmother’s attic, she found an ancient, worn-out book. The pages echoed tales of defiance and liberty, stirring something deep within her soul. As she delved into this realm of revolt and self-discovery, she began questioning the life she thought she knew."

4. "Logic" editor's output (given passage #4):

"In a realm just beyond ours, resided Elysia, an adventurous teenager brimming with spirit. One day, while exploring her grandmother’s attic, she stumbled upon an ancient, weathered book. Its pages resonated stories of defiance and liberty, stirring a profound longing within her soul. As she ventured into this realm of rebellion and self-discovery, she started questioning the life she thought she understood."

Note: The changes made are minor but significant. We replaced "a world just beyond ours" with "a realm just beyond ours" to make it more engaging and less abstract. Also, we changed "thought she knew" to "understood" for better clarity.
