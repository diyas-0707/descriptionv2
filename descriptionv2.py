import streamlit as st
from openai import OpenAI
client = OpenAI()


def get_hint(level):
    """Generate a descriptive hint for a random object using OpenAI."""
    difficulty = "very easy" if level <= 3 else "easy" if level <= 7 else "moderate"
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a game master."},
            {
                "role": "user",
                "content": (
                    f"You are creating a quiz game for students. "
                    f"Generate a hint for a random object at {difficulty} difficulty level. "
                    "The correct answer must be one word. Format your response as 'HINT: ANSWER: '. "
                    "Be descriptive but not too revealing. Only use two sentences for the hint. No questions can repeat or have the same answer ever, even in different games."
                ),
            },
        ],
    )
    response = completion.choices[0].message.content
    hint_part = response.split("ANSWER:")[0].replace("HINT:", "").strip()
    answer_part = response.split("ANSWER:")[1].strip().lower()
    return hint_part, answer_part


def start_game():
    """Initialize the game session."""
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.hint = None
    st.session_state.answer = None
    st.session_state.solved = False
    st.session_state.gave_up = False
    st.session_state.game_complete = False
    st.session_state.show_next = False
    st.session_state.show_wrong = False
    advance_level()


def advance_level():
    """Advance to the next level and get a new hint."""
    if st.session_state.level <= 10:
        hint, answer = get_hint(st.session_state.level)
        st.session_state.hint = hint
        st.session_state.answer = answer
        st.session_state.solved = False
        st.session_state.gave_up = False
        st.session_state.show_next = False
        st.session_state.show_wrong = False
    else:
        st.session_state.game_complete = True


# Initialize session state
if 'level' not in st.session_state:
    start_game()


# Streamlit UI
st.title("Guessing Game")


if not st.session_state.game_complete:
    st.write(f"Question {st.session_state.level}/10")
    st.subheader("Here's your hint:")
    st.write(st.session_state.hint)


    if not st.session_state.show_next:
        guess_input = st.text_input(
            "What's your guess?",
            value="",
            key=f"guess_input_{st.session_state.level}"
        )


        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Guess", key=f"submit_{st.session_state.level}"):
                if guess_input.strip():  # Only process non-empty input
                    if guess_input.lower() == st.session_state.answer:
                        st.success("🎉 Correct!")
                        st.session_state.score += 1
                        st.session_state.solved = True
                        st.session_state.show_next = True
                    else:
                        st.error("❌ Wrong answer! Try again.")
                        st.session_state.show_wrong = True
        with col2:
            if st.button("Give Up", key=f"give_up_{st.session_state.level}"):
                st.warning(f"The correct answer was: **{st.session_state.answer}**")
                st.session_state.gave_up = True
                st.session_state.show_next = True


    if st.session_state.show_next:
        if st.button("Next", key=f"next_{st.session_state.level}"):
            st.session_state.level += 1
            advance_level()
            st.rerun() #this is the line that I replaced. It used to have "st.session_state.show_next = False"
else:
    st.success("🎉 You've completed the quiz!")
    st.write(f"Your final score is **{st.session_state.score}/10**.")
    st.balloons()