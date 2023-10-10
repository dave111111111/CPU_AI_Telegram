from chunkipy import TextChunker, TokenEstimator
from transformers import AutoTokenizer
from transformers import pipeline

# Initialize the summarization pipeline with the BART model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarizing_text(text, min_summary_percentage, max_summary_percentage):
    class BertTokenEstimator(TokenEstimator):
        def __init__(self):
            self.bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

        def estimate_tokens(self, text):
            return len(self.bert_tokenizer.encode(text))

    # Create an instance of the BertTokenEstimator
    bert_token_estimator = BertTokenEstimator()

    # Create a TextChunker instance with token-based segmentation
    text_chunker = TextChunker(512, tokens=True, token_estimator=bert_token_estimator)

    # Lists to store the chunks and their summaries
    chunks = text_chunker.chunk(text)
    summarized_chunks = []

    # Define the desired summary length range as percentages (e.g., 30% to 70%)
    for i, chunk in enumerate(chunks):
        chunk_text = chunk
        num_tokens = bert_token_estimator.estimate_tokens(chunk_text)

        min_summary_length = int(0.01 * min_summary_percentage * num_tokens)  # Convert percentage to tokens
        max_summary_length = int(0.01 * max_summary_percentage * num_tokens)  # Convert percentage to tokens

        # Ensure that max_summary_length is not greater than the input text's token count
        max_summary_length = min(max_summary_length, num_tokens)

        # Summarize the chunk with the defined length range
        summary = summarizer(chunk_text, min_length=min_summary_length, max_length=max_summary_length, do_sample=False)

        # Extract and print the summarized text
        summarized_text = summary[0]['summary_text']
        summarized_chunks.append(summarized_text)

    return summarized_chunks

def count_summary_words(summary):
    words = summary.split()
    n_words = len(words)
    return n_words

def summarize_main(text, min_summary_percentage, max_summary_percentage):

    # Example usage:
    words = text.split()
    n_words = len(words)
    min_length = int(n_words * min_summary_percentage / 100)
    max_length = int(n_words * max_summary_percentage / 100)
    cleaned_summaries = []  # Create a list to store cleaned summaries

    summary = summarizing_text(text, min_summary_percentage=min_summary_percentage, max_summary_percentage=max_summary_percentage)
    # Extract and add the cleaned summarized text without brackets and quotes for each chunk to the list
    for summarized_chunk in summary:
        summarized_text = summarized_chunk.strip("[]\"")
        cleaned_summaries.append(summarized_text)

    summary_word_count = 0
    for i, summarized_chunk in enumerate(summary):
        words_x_chunk = count_summary_words(summarized_chunk)
        summary_word_count += words_x_chunk
    print("expected min length:", min_length, "\n")
    print("expected max length:", max_length, "\n")
    print("Summary word count:", summary_word_count)
    return cleaned_summaries

"""
text = "The Chicago Bulls: A Legacy of Excellence"The Chicago Bulls, an iconic franchise in the National Basketball Association (NBA), have left an indelible mark on the world of sports and pop culture. Founded in 1966, this storied team has achieved unprecedented success, captivating fans and inspiring generations. This text delves into the rich history, memorable moments, legendary players, and the enduring legacy of the Chicago Bulls.Founding Years and Early Struggles:The Chicago Bulls entered the NBA as an expansion team in 1966. Their early years were marked by challenges and struggles as they sought to establish themselves in the league. However, in 1969, the Bulls drafted a talented player named Jerry Sloan, who would become one of the franchise's first stars. Despite these early struggles, the team's foundation was being built.The Arrival of Michael Jordan:The turning point for the Chicago Bulls came in 1984 when they selected Michael Jordan as the third overall pick in the NBA Draft. This decision would alter the course of the franchise and the history of basketball itself. Jordan, often considered the greatest player in NBA history, led the Bulls to six NBA championships during the 1990s. His scoring ability, work ethic, and competitiveness were unparalleled, making him a global basketball icon.The 1990s Dynasty:Under the guidance of head coach Phil Jackson, and with Jordan, Scottie Pippen, and Dennis Rodman on the roster, the Chicago Bulls embarked on a historic journey. They won six NBA championships in the 1990s (1991, 1992, 1993, 1996, 1997, and 1998), establishing themselves as one of the most dominant teams in sports history. The team's unmatched success made "Bulls" synonymous with winning and excellence.Phil Jackson's Zen Master Approach:Phil Jackson's coaching philosophy played a pivotal role in the Bulls' dynasty. His unique approach, often described as the "Zen Master" philosophy, combined mindfulness, teamwork, and tactical brilliance. Jackson's influence on the team's success cannot be overstated, as he masterfully managed the personalities of the Bulls' stars and role players.The Flu Game and Other Iconic Moments:Michael Jordan's career with the Bulls is a treasure trove of unforgettable moments. The "Flu Game" during the 1997 NBA Finals, in which Jordan overcame illness to lead the Bulls to victory, remains one of the most legendary performances in sports history. The Bulls' Finals appearances were replete with iconic highlights, and their victories are etched in the annals of basketball lore.Post-Jordan Era and the Rebuild:After Jordan's second retirement in 1998, the Bulls faced the challenging task of rebuilding. They went through several seasons of struggles and roster changes. However, during this period, a new generation of players emerged, including Derrick Rose, who won the NBA MVP award in 2011. Rose's athleticism and leadership briefly rekindled the excitement in Chicago.Return to Prominence:The 2010s witnessed the Bulls' resurgence. Led by coach Tom Thibodeau and a talented roster that included Rose, Joakim Noah, and Luol Deng, the team consistently reached the playoffs. In 2011, they achieved the best record in the NBA during the regular season, rekindling hope for a return to championship glory. Although injuries posed challenges, the Bulls displayed a determination to compete at the highest level.Current State and Future Prospects:As of my knowledge cutoff date in September 2021, the Chicago Bulls have continued their efforts to build a competitive team. They made significant offseason acquisitions, including acquiring DeMar DeRozan and Lonzo Ball, signaling their commitment to returning to the playoffs. The passionate fan base remains dedicated to the team, eager for a new era of success.Cultural Impact and Legacy:The Chicago Bulls transcended the sport of basketball, leaving an indelible mark on popular culture. The team's iconic red, black, and white colors, along with its iconic logo, became symbols of excellence. Michael Jordan's impact extended beyond sports, influencing fashion, advertising, and the global perception of basketball. The Air Jordan sneaker line, for example, became a fashion staple.In conclusion, the Chicago Bulls are more than a basketball team; they are a symbol of determination, excellence, and the enduring pursuit of greatness. From their early struggles to their dynastic years and the cultural phenomenon they became, the Bulls' legacy is etched in history. As they continue to evolve and strive for success, their iconic status remains a testament to the power of sport to inspire and unite people around the world."

# Define the minimum and maximum summary percentage
min_summary_percentage = 40
max_summary_percentage = 70

# Call the summarize_main function
summary = summarize_main(text, min_summary_percentage, max_summary_percentage)

print(summary)"""