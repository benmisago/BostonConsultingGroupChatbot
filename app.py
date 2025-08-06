from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

data = [
    {"Company": "Apple", "Year": 2022, "Total Revenue": 394328, "Net Income": 99803, "Total Assets": 352755, "Total Liabilities": 302083, "Cash Flow from Operations": 122151},
    {"Company": "Apple", "Year": 2021, "Total Revenue": 365817, "Net Income": 94680, "Total Assets": 351002, "Total Liabilities": 287912, "Cash Flow from Operations": 104038},
    {"Company": "Apple", "Year": 2020, "Total Revenue": 274515, "Net Income": 57411, "Total Assets": 323888, "Total Liabilities": 105392, "Cash Flow from Operations": 80674},
    {"Company": "Tesla", "Year": 2024, "Total Revenue": 97690, "Net Income": 7091, "Total Assets": 122070, "Total Liabilities": 48390, "Cash Flow from Operations": 14923},
    {"Company": "Tesla", "Year": 2023, "Total Revenue": 96773, "Net Income": 14997, "Total Assets": 106618, "Total Liabilities": 43009, "Cash Flow from Operations": 13256},
    {"Company": "Tesla", "Year": 2022, "Total Revenue": 81462, "Net Income": 12556, "Total Assets": 4828, "Total Liabilities": 2215, "Cash Flow from Operations": 14724},
    {"Company": "Microsoft", "Year": 2024, "Total Revenue": 245122, "Net Income": 88136, "Total Assets": 512163, "Total Liabilities": 243686, "Cash Flow from Operations": 118548},
    {"Company": "Microsoft", "Year": 2023, "Total Revenue": 211915, "Net Income": 72361, "Total Assets": 411976, "Total Liabilities": 205753, "Cash Flow from Operations": 87582},
    {"Company": "Microsoft", "Year": 2022, "Total Revenue": 198270, "Net Income": 72738, "Total Assets": 364840, "Total Liabilities": 198298, "Cash Flow from Operations": 89035},
]

df = pd.DataFrame(data)
df = df.sort_values(by=['Company', 'Year']).reset_index(drop=True)

df['Revenue Growth (%)'] = df.groupby('Company')['Total Revenue'].pct_change() * 100
df['Net Income Growth (%)'] = df.groupby('Company')['Net Income'].pct_change() * 100
df['Total Assets Growth (%)'] = df.groupby('Company')['Total Assets'].pct_change() * 100
df['Total Liabilities Growth (%)'] = df.groupby('Company')['Total Liabilities'].pct_change() * 100
df['Cash Flow Growth (%)'] = df.groupby('Company')['Cash Flow from Operations'].pct_change() * 100

companies = sorted(df['Company'].unique())

def simple_chatbot(user_query):
    user_query = user_query.lower()
    if "total revenue" in user_query:
        return "The total revenue is $394.3 billion."
    elif "net income" in user_query:
        return "The net income has increased by 5.4% over the last year."
    elif "gross profit margin" in user_query:
        return "The gross profit margin is 42%."
    elif "main expenses" in user_query:
        return "The main expenses are R&D, Marketing, and Operations."
    elif "ebitda" in user_query:
        return "The EBITDA is $120 billion."
    else:
        return "Sorry, I can only provide information on predefined queries."

HTML_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Financial ChatBot</title>
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
  <style>
    body {
      background: #f8f9fa;
    }
    .chatbot-container {
      max-width: 600px;
      margin: 50px auto 70px;
      background: white;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.1);
      text-align: center;
    }
    h1 {
      font-weight: 500;
      margin-bottom: 15px;
      color: #3e8440;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 15px;
    }
    #logo {
      width: 100px;
      height: 100px;
      object-fit: contain;
      cursor: pointer;
      user-select: none;
      transition: transform 0.3s ease;
    }
    .response-box {
      background: #e9f5ff;
      border-left: 5px solid #0d6efd;
      padding: 15px 20px;
      border-radius: 8px;
      margin-top: 20px;
      font-size: 1.1rem;
      color: #0d6efd;
      font-weight: 500;
      text-align: left;
    }
    .form-control:focus {
      box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
      border-color: #0d6efd;
    }
    .how-to-use {
      background: #fff3cd;
      border: 1px solid #ffeeba;
      padding: 20px 25px;
      border-radius: 8px;
      margin-top: 40px;
      color: #856404;
      font-size: 0.95rem;
      line-height: 1.5;
      text-align: left;
    }
    .how-to-use h2 {
      color: #856404;
      margin-bottom: 15px;
      font-weight: 600;
    }
    .how-to-use ul {
      padding-left: 20px;
    }
  </style>
</head>
<body>
  <div class="chatbot-container shadow-sm" role="main" aria-label="BCG Financial ChatBot">
    <h1 id="title">
      <img src="{{ url_for('static', filename='BCG_MONOGRAM.png') }}" alt="BCG Logo" id="logo" />
      BCG Financial ChatBot
    </h1>
    <form action="/ask" method="post" class="d-flex gap-2" role="search" aria-label="Ask a financial question">
      <input type="text" name="query" placeholder="Ask a question..." class="form-control" autocomplete="off" required aria-required="true" />
      <button type="submit" class="btn btn-primary" aria-label="Submit question">Ask</button>
    </form>

    {% if response %}
      <div class="response-box" role="alert" aria-live="polite">
        {{ response }}
      </div>
    {% endif %}

    <section class="how-to-use" aria-label="How to use the chatbot">
      <h2>How to Use</h2>
      <p>Try asking questions related to the following topics:</p>
      <ul>
        <li><strong>Total revenue</strong> — e.g., "What is the total revenue?"</li>
        <li><strong>Net income</strong> — e.g., "Tell me the net income."</li>
        <li><strong>Gross profit margin</strong> — e.g., "What’s the gross profit margin?"</li>
        <li><strong>Main expenses</strong> — e.g., "What are the main expenses?"</li>
        <li><strong>EBITDA</strong> — e.g., "What is the EBITDA?"</li>
      </ul>
      <p><em>Note: The chatbot only understands predefined queries for now.</em></p>
    </section>

    <section class="how-to-use" aria-label="Companies covered">
      <h2>Companies Covered</h2>
      <p>This chatbot provides financial information about the following companies:</p>
      <ul>
        {% for company in companies %}
          <li>{{ company }}</li>
        {% endfor %}
      </ul>
    </section>
  </div>

  <!-- Bootstrap JS Bundle -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

  <!-- GSAP -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <script>
    // Animate the title: subtle bounce on load
    gsap.fromTo("#title", 
      { y: -20, opacity: 0 }, 
      { y: 0, opacity: 1, duration: 1, ease: "bounce.out" }
    );

    // Logo hover scale animation (smaller scale)
    const logo = document.getElementById("logo");
    logo.addEventListener("mouseenter", () => {
      gsap.to(logo, { scale: 1.1, duration: 0.3, ease: "power1.out" });
    });
    logo.addEventListener("mouseleave", () => {
      gsap.to(logo, { scale: 1, duration: 0.3, ease: "power1.out" });
    });

    // Logo gentle infinite bounce (smaller bounce)
    gsap.to("#logo", {
      y: -8,
      duration: 2,
      ease: "power1.inOut",
      repeat: -1,
      yoyo: true,
      delay: 1.5
    });
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE, response=None, companies=companies)

@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.form.get("query", "")
    response = simple_chatbot(user_query)
    return render_template_string(HTML_PAGE, response=response, companies=companies)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
