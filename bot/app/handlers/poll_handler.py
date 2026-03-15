from aiogram.types import Message, PollAnswer
from aiogram.filters import Command
from aiogram import Bot, Router

router = Router()

poll_storage = {}

@router.message(Command("vote"))
async def send_vote(message: Message, bot: Bot):
    question = "Когда провести мероприятие?"
    options = ["Пятница", "Суббота", "Воскресенье"]

    poll = await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=options,
        is_anonymous=False,  # важно для отслеживания пользователей
        allows_multiple_answers=False
    )

    # сохраняем poll_id, варианты и пустой словарь голосов
    poll_storage[poll.poll.id] = {"options": options, "votes": {}}


@router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer):
    poll_id = poll_answer.poll_id
    user = poll_answer.user
    option_ids = poll_answer.option_ids

    if poll_id not in poll_storage or not option_ids:
        return

    # сохраняем голос пользователя
    poll_storage[poll_id]["votes"][user.id] = option_ids[0]

    option_text = poll_storage[poll_id]["options"][option_ids[0]]
    print(f"Пользователь {user.full_name} (id={user.id}) проголосовал за: {option_text}")


@router.message(Command("results"))
async def show_results(message: Message):
    if not poll_storage:
        await message.answer("Пока нет активных опросов.")
        return

    results_text = "📊 Результаты опросов:\n\n"

    for poll_id, data in poll_storage.items():
        options = data["options"]
        votes = data["votes"]

        # считаем количество голосов за каждый вариант
        option_counts = [0] * len(options)
        for vote in votes.values():
            option_counts[vote] += 1

        results_text += "Опрос:\n"
        for idx, option in enumerate(options):
            results_text += f"{option}: {option_counts[idx]} голосов\n"
        results_text += "\n"

    await message.answer(results_text)