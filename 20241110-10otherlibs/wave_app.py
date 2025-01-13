from h2o_wave import main, app, Q, ui, data  # Note: main must be imported even though it is not used.

@app("/")
async def serve(q: Q):
    q.page["title"] = ui.header_card(
        box="1 1 10 1",
        title="Realtime dashboard",
        subtitle="Hello DataFans",
        image="https://wave.h2o.ai/img/h2o-logo.svg",
    )
    q.page['select'] = ui.form_card(
        box='1 2 2 2', 
        items=[
        ui.dropdown(
            name='dropdown', 
            label='Select Category', 
            choices=[
                ui.choice(name='Safari', label='Safari'),
                ui.choice(name='Chrome', label='Chrome'),
                ui.choice(name='Firefox', label='Firefox'),
            ],
        )]
    )
    q.page["counter"] = ui.large_stat_card(
        box="3 2 2 2",
        title="Counter",
        value="={{i}}",
        aux_value="points received",
        data={ "i": 0 },
        caption="Number of points received from script",
    )
    q.page['plot'] = ui.plot_card(
        box='1 4 10 5',
        title='Web Browser Ratio',
        data=data('counter browser amount', -3*20, rows=[]),
        plot=ui.plot([
            ui.mark(type='interval', x='=counter', y='=amount', color='=browser', stack='auto', y_min=0)
        ]),
    )

    await q.page.save()
