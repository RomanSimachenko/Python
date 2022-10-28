import database
import monitoring


async def auto_monitoring(bot, time: str):
    users = await database.start_auto_monitoring(time)
    
    for user in users:
        await bot.send_message(user.chat_id, "📌 Автоматичний моніторинг: ")
        for university in user.universities.split(','):
            un = await monitoring.process_un(university, user.k_bal)
            await bot.send_message(user.chat_id, f"\
{un.name}({un.url}): \nВсього {un.k_higher} \
абітурієнтів із {un.k_all} мають конкурсний бал вище \
або рівний {user.k_bal}, серед них: {un.k_kv} із квотою та {un.k_k} на контракт"
)

            if user.result_view == 'with_list':
                await bot.send_message(user.chat_id, "\
№ Призвіще та ініціали | Пріорітет | Конкурсний бал | Квота(+/-) | Бюджет(Б)/Контракт(К)\
")
                result_list = ""
                for index, entrant in enumerate(un.entrants):
                    result_list += f"\
{index + 1}. {entrant.full_name} | {entrant.priority} | {entrant.k_bal} | {entrant.kvota} | {entrant.b_or_k}\n\
"
                    if (index + 1) % 50 == 0:
                        await bot.send_message(user.chat_id, result_list)
                        result_list = ""
                await bot.send_message(user.chat_id, result_list)
