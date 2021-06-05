ate `FIRST` now
    return FIRST


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [CallbackQueryHandler(guide, pattern='on_guide'),
                    CallbackQueryHandler(traff_inf, pattern='on_traffic'),
                    ],
            1: [MessageHandler(Filters.text & ~(Filters.command), town, pass_user_data=True)],
            2: [MessageHandler(Filters.text & ~(Filters.command), interests,
                               pass_user_data=True),
                CallbackQueryHandler(change_places, pass_user_data=True),
                # CallbackQueryHandler(start_over, pattern='on_menu'),

                ],
            3: [MessageHandler(Filters.text & ~(Filters.command), traffic,
                               pass_user_data=True), ]

        },
        fallbacks=[CommandHandler('start', start)]
    )
    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
