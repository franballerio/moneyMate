# Money Mate 🤖💸 Your Friendly Pocket Accountant!

Ever feel like your bank app just doesn't *get* you? Tired of squinting at confusing statements to figure out where your money went? That's exactly why Money Mate was born!

I created Money Mate after landing my first job and realizing I needed a super simple, no-fuss way to keep an eye on my spending. Now, tracking your expenses is as easy as sending a quick chat to your new financial buddy!

## What Can Money Mate Do For You? ✨

Think of Money Mate as your personal finance assistant, always ready to help right within Telegram:

* **Log Expenses in a Snap!** 💨
    Just tell Money Mate what you bought, how much it was, and the category. Easy peasy!
    * Example: `Coffee, 3.50, Food` or `/add Lunch with friends, 25, Social`
    * Money Mate is smart enough to understand item names with spaces!
    * You'll get a neat confirmation for every expense added.

* **See Where Your Money Goes!** 📊
    Curious about your spending? Money Mate can show you the totals or a list of your expenses.
    * `/total`: See how much you've spent today.
    * `/total 5 2024`: Check your spending for May 2024.
    * `/spent`: Get a list of today's expenses.
    * `/spent 26 5 2024`: See all items you bought on May 26, 2024.

* **Become a Budgeting Boss!** 🎯
    Want to save more? Set spending goals for different categories.
    * `/budget Groceries 300` (Sets a $300 budget for Groceries)
    * Money Mate will even give you a friendly heads-up if you're about to go over budget!

* **Oops! Made a Mistake?** 🔙
    * `/undo`: Quickly remove the last expense you added. No worries!

* **Know Your Habits!** 📝
    * `/categories`: See a list of all the spending categories you've used.

* **For the Curious (and Developers!):**
    * `/simulate`: Want to see Money Mate in action with lots of data? This command fills it up with random expenses.
    * `/restart`: Need a fresh start? This clears all your expense data (use this one carefully!).

## Getting Started with Your Money Mate 🚀

Want to bring Money Mate to life on your own Telegram? If you're a bit tech-savvy, here’s how:

1.  **Grab the Code:**
    You'll need to clone this project's repository from wherever it's hosted (e.g., GitHub).
    ```bash
    git clone <your-repository-url>
    cd moneyMate
    ```

2.  **Set Up a Cozy Corner for It (Virtual Environment):**
    It’s good practice to keep project things tidy.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the Magic Ingredients:**
    Money Mate needs a few tools to work.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Give Money Mate Its Keys:**
    Create a file named `.env` inside the `src/bot/` folder. This is where you'll put your secret Telegram bot token and decide where to save your data.
    ```env
    telegram_bot_api=YOUR_SUPER_SECRET_TELEGRAM_BOT_TOKEN
    database_name=data/mymoney.db # This is where your expense info will live
    ```
    *(Money Mate will try to create the `data` folder if it's not there!)*

5.  **Wake Up Money Mate!**
    ```bash
    python src/bot/main_bot.py
    ```
    And that's it! Your very own Money Mate should be up and running, ready to chat on Telegram.

## What Makes Money Mate Tick? (The Techy Bits, Briefly!) ⚙️

Money Mate is built with some cool Python tools:
* **Python**: The main language.
* **python-telegram-bot**: Lets it talk to Telegram.
* **Pandas & NumPy**: Help with data, especially for the `/simulate` feature.
* **SQLite**: A neat little database that stores all your expenses right on your system.

## Dream Big: Future Ideas for Money Mate! 🌠

Money Mate is already pretty handy, but here are some cool things it could learn to do:
* **Picture This!** Show pretty charts of your spending.
* **Set & Forget:** Handle those monthly subscriptions automatically.
* **Show Me the Money!** Track your income too.
* **Chat Naturally:** Understand dates like "yesterday" or "last Tuesday."
* **Button Magic:** Use cool Telegram buttons for even quicker actions.
* **Speak Your Language:** Offer Money Mate in more languages.

## Want to Help Money Mate Grow? 🌱

Got ideas? Found a bug? Feel free to jump in! This is a friendly project, and new ideas or help are always welcome.

---

Hope this version feels more engaging and user-friendly!