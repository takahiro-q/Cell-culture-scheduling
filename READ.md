# Cell-culture-scheduling

## 入力内容

## EXPERIMENT_STEPS

- Step(Chr): 培養工程のステップ(ex.iPS細胞培養、FloorPlate誘導、といった項目を記入)
- Duration(Int)： 培養期間を記入する
- Medium(Chr): 使用している培地を記入する
- Compounds(Chr): 使用している化合物を記入する
- Step, Duration, Medium, Compoundsの項目を追加："continue?", ("Yes", "No")
    - "continue?", ("Yes")　=>　次のStep, Duration, Medium, Compoundsの項目が追加される
    - "continue?", ("No")　=> 終了：データフレームが作製される

>データフレームが作成される

## Y/M/Dボックス

- year(Int): 年を記入(min_value=2000, max_value=2099に設定されている)
- month(Int): 月を記入する(min_value=1, max_value=12に設定されている)
- day(Int): 日を記入する(min_value=1, max_value=31)
- start_date: 記入したyear, month, dayが格納される

- days_to_start: 工程ステップの作業開始日時
- days_to_end: 工程ステップの作業終了日時
- task_duration: 工程ステップの作業期間

- schedule_plot: 工程のガンチャート。x軸は日付で3日間ごとで示されている。
