#!python3
# coding: utf-8

"""
フィールドはカンマで区切り、行は改行で分けるノーマルなcsvを扱うモジュール
    csvデータからTwoDimArrayを作成し二次元配列として処理する

    ※セパレータはデフォルトでカンマとなっているが、任意に指定可能で正規表現も指定できる
    ※フィールドの左右の空白は無視する('  hoge fuga  ' -> 'hoge fuga')
"""

#----------------------------------------------------------------------------------------------------
#   使用例
#       >>> import csv_normal as csv
#
#       #sample.csvファイルからcsvデータを読み込み、TwoDimArray(二次元配列)を作成
#       >>> c = csv.load('sample.csv', encoding='utf8')
#
#
#       #行列のサイズを確認
#       >>> c.shape()
#       (7, 8)
#
#
#       #print関数でTwoDimArrayを行列表示(先頭5行まで表示し、残りは省略表示する)
#       >>> print(c)
#       Name   , Strength   , Buttle Power, Birthdate   , Sex   , Race     , Height(cm), Weight(kg)
#       Goku   , very strong,    3_000_000, Age-737-year, Male  , Saiyan   ,        175,         62
#       Vegeta , very strong,    2_000_000, Age-732-year, Male  , Saiyan   ,        164,         56
#       Piccolo, strong     ,    1_000_000, Age-753-year, Male  , Namekian ,        226,        116
#       Bulma  , very weak  ,            3, Age-733-year, Female, Earthling,        165,         49
#       ↓(There are 2 rows)
#       
#
#       #printメソッドでTwoDimArrayを行列表示(全データを表示する)
#       >>> c.print()
#       Name   , Strength   , Buttle Power, Birthdate   , Sex   , Race     , Height(cm), Weight(kg)
#       Goku   , very strong,    3_000_000, Age-737-year, Male  , Saiyan   ,        175,         62
#       Vegeta , very strong,    2_000_000, Age-732-year, Male  , Saiyan   ,        164,         56
#       Piccolo, strong     ,    1_000_000, Age-753-year, Male  , Namekian ,        226,        116
#       Bulma  , very weak  ,            3, Age-733-year, Female, Earthling,        165,         49
#       Krillin, good       ,       75_000, Age-736-year, Male  , Earthling,        153,         45
#       Yamcha , weak       ,        1_480, Age-733-year, Male  , Earthling,        183,         68
#       
#
#       #printメソッドはTwoDimArrayの表示範囲を選択できる
#       >>> c.print(3)
#       Name  , Strength   , Buttle Power, Birthdate   , Sex , Race  , Height(cm), Weight(kg)
#       Goku  , very strong,    3_000_000, Age-737-year, Male, Saiyan,        175,         62
#       Vegeta, very strong,    2_000_000, Age-732-year, Male, Saiyan,        164,         56
#       ↓(There are 4 rows)
#       
#       
#       #print2メソッドはTwoDimArrayを枠で囲んで表示する(表示範囲の選択も可能)
#       >>> c.print2()
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Name    |Strength    |Buttle Power|Birthdate   |Sex   |Race      |Height(cm)|Weight(kg)|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Goku    |very strong |   3_000_000|Age-737-year|Male  |Saiyan    |       175|        62|
#       +--------+            +------------+------------+      +          +----------+----------+
#       |Vegeta  |very strong |   2_000_000|Age-732-year|Male  |Saiyan    |       164|        56|
#       +--------+------------+------------+------------+      +----------+----------+----------+
#       |Piccolo |strong      |   1_000_000|Age-753-year|Male  |Namekian  |       226|       116|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Bulma   |very weak   |           3|Age-733-year|Female|Earthling |       165|        49|
#       +--------+------------+------------+------------+------+          +----------+----------+
#       |Krillin |good        |      75_000|Age-736-year|Male  |Earthling |       153|        45|
#       +--------+------------+------------+------------+      +          +----------+----------+
#       |Yamcha  |weak        |       1_480|Age-733-year|Male  |Earthling |       183|        68|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       
#       
#       #デフォルト設定では枠のグループ化機能が有効になっているため、
#       #隣接するフィールド値が同じ場合は境界の枠が消えてグループ化される
#       #
#       #   border_grouping: Falseで枠のグループ化機能を無効にできる
#       #
#       >>> c.border_grouping = False
#       >>> c.print2()
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Name    |Strength    |Buttle Power|Birthdate   |Sex   |Race      |Height(cm)|Weight(kg)|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Goku    |very strong |   3_000_000|Age-737-year|Male  |Saiyan    |       175|        62|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Vegeta  |very strong |   2_000_000|Age-732-year|Male  |Saiyan    |       164|        56|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Piccolo |strong      |   1_000_000|Age-753-year|Male  |Namekian  |       226|       116|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Bulma   |very weak   |           3|Age-733-year|Female|Earthling |       165|        49|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Krillin |good        |      75_000|Age-736-year|Male  |Earthling |       153|        45|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Yamcha  |weak        |       1_480|Age-733-year|Male  |Earthling |       183|        68|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       
#       
#       #デフォルト設定では数字の区切り文字表示機能(千倍ごとにアンダースコアで数字を区切る)が有効になっている
#       #※数値リテラル内のアンダースコアはPython3.6から追加された新機能
#       #
#       #   grouping_opt: Falseで数字の区切り文字表示機能を無効にできる
#       #
#       >>> c.grouping_opt = False
#       >>> c.print2()
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Name    |Strength    |Buttle Power|Birthdate   |Sex   |Race      |Height(cm)|Weight(kg)|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Goku    |very strong |     3000000|Age-737-year|Male  |Saiyan    |       175|        62|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Vegeta  |very strong |     2000000|Age-732-year|Male  |Saiyan    |       164|        56|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Piccolo |strong      |     1000000|Age-753-year|Male  |Namekian  |       226|       116|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Bulma   |very weak   |           3|Age-733-year|Female|Earthling |       165|        49|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Krillin |good        |       75000|Age-736-year|Male  |Earthling |       153|        45|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Yamcha  |weak        |        1480|Age-733-year|Male  |Earthling |       183|        68|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       
#       
#       #print2_borderプロパティで枠の種類を変えられる
#       >>> c.print2_border = 'Simple'
#       >>> c.print2()
#        Name     Strength     Buttle Power Birthdate    Sex    Race       Height(cm) Weight(kg) 
#        -------- ------------ ------------ ------------ ------ ---------- ---------- ---------- 
#        Goku     very strong       3000000 Age-737-year Male   Saiyan            175         62 
#        Vegeta   very strong       2000000 Age-732-year Male   Saiyan            164         56 
#        Piccolo  strong            1000000 Age-753-year Male   Namekian          226        116 
#        Bulma    very weak               3 Age-733-year Female Earthling         165         49 
#        Krillin  good                75000 Age-736-year Male   Earthling         153         45 
#        Yamcha   weak                 1480 Age-733-year Male   Earthling         183         68
#       
#       
#       >>> c.print2_border = 'Psql'
#       >>> c.print2()
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Name    |Strength    |Buttle Power|Birthdate   |Sex   |Race      |Height(cm)|Weight(kg)|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Goku    |very strong |     3000000|Age-737-year|Male  |Saiyan    |       175|        62|
#       |Vegeta  |very strong |     2000000|Age-732-year|Male  |Saiyan    |       164|        56|
#       |Piccolo |strong      |     1000000|Age-753-year|Male  |Namekian  |       226|       116|
#       |Bulma   |very weak   |           3|Age-733-year|Female|Earthling |       165|        49|
#       |Krillin |good        |       75000|Age-736-year|Male  |Earthling |       153|        45|
#       |Yamcha  |weak        |        1480|Age-733-year|Male  |Earthling |       183|        68|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       
#       
#       #枠は簡単にカスタマイズ可能
#       >>> csv.border_patterns['Custom1']="""
#       o-o-o
#       | | |
#       o-o-o
#       | | |
#       o-o-o
#       """
#       >>> c.print2_border = 'Custom1'
#       >>> c.print2()
#       o--------o------------o------------o------------o------o----------o----------o----------o
#       |Name    |Strength    |Buttle Power|Birthdate   |Sex   |Race      |Height(cm)|Weight(kg)|
#       o--------o------------o------------o------------o------o----------o----------o----------o
#       |Goku    |very strong |     3000000|Age-737-year|Male  |Saiyan    |       175|        62|
#       o--------o------------o------------o------------o------o----------o----------o----------o
#       |Vegeta  |very strong |     2000000|Age-732-year|Male  |Saiyan    |       164|        56|
#       o--------o------------o------------o------------o------o----------o----------o----------o
#       |Piccolo |strong      |     1000000|Age-753-year|Male  |Namekian  |       226|       116|
#       o--------o------------o------------o------------o------o----------o----------o----------o
#       |Bulma   |very weak   |           3|Age-733-year|Female|Earthling |       165|        49|
#       o--------o------------o------------o------------o------o----------o----------o----------o
#       |Krillin |good        |       75000|Age-736-year|Male  |Earthling |       153|        45|
#       o--------o------------o------------o------------o------o----------o----------o----------o
#       |Yamcha  |weak        |        1480|Age-733-year|Male  |Earthling |       183|        68|
#       o--------o------------o------------o------------o------o----------o----------o----------o
#       
#       
#       #reset_propertyメソッドで各プロパティの設定をリセットできる
#       >>> c.reset_property()
#       >>> c.print2()
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Name    |Strength    |Buttle Power|Birthdate   |Sex   |Race      |Height(cm)|Weight(kg)|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Goku    |very strong |   3_000_000|Age-737-year|Male  |Saiyan    |       175|        62|
#       +--------+            +------------+------------+      +          +----------+----------+
#       |Vegeta  |very strong |   2_000_000|Age-732-year|Male  |Saiyan    |       164|        56|
#       +--------+------------+------------+------------+      +----------+----------+----------+
#       |Piccolo |strong      |   1_000_000|Age-753-year|Male  |Namekian  |       226|       116|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Bulma   |very weak   |           3|Age-733-year|Female|Earthling |       165|        49|
#       +--------+------------+------------+------------+------+          +----------+----------+
#       |Krillin |good        |      75_000|Age-736-year|Male  |Earthling |       153|        45|
#       +--------+------------+------------+------------+      +          +----------+----------+
#       |Yamcha  |weak        |       1_480|Age-733-year|Male  |Earthling |       183|        68|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       
#       
#       #行と列のインデックスの表示が可能(表示範囲の選択も可能)
#       >>> c.print_idx()
#       index, 0      , 1          , 2           , 3           , 4     , 5        , 6         , 7         , index
#           0, Name   , Strength   , Buttle Power, Birthdate   , Sex   , Race     , Height(cm), Weight(kg), 0    
#           1, Goku   , very strong,    3_000_000, Age-737-year, Male  , Saiyan   ,        175,         62, 1    
#           2, Vegeta , very strong,    2_000_000, Age-732-year, Male  , Saiyan   ,        164,         56, 2    
#           3, Piccolo, strong     ,    1_000_000, Age-753-year, Male  , Namekian ,        226,        116, 3    
#           4, Bulma  , very weak  ,            3, Age-733-year, Female, Earthling,        165,         49, 4    
#           5, Krillin, good       ,       75_000, Age-736-year, Male  , Earthling,        153,         45, 5    
#           6, Yamcha , weak       ,        1_480, Age-733-year, Male  , Earthling,        183,         68, 6    
#       index, 0      , 1          , 2           , 3           , 4     , 5        , 6         , 7         , index
#       
#
#       #さらに枠で囲んで見やすく表示可能(表示範囲の選択も可能)
#       >>> c.print_idx2()
#         index:0       :1           :2           :3           :4     :5         :6         :7         :index  
#        ......+--------+------------+------------+------------+------+----------+----------+----------+...... 
#             0|Name    |Strength    |Buttle Power|Birthdate   |Sex   |Race      |Height(cm)|Weight(kg)|0      
#        ......+--------+------------+------------+------------+------+----------+----------+----------+...... 
#             1|Goku    |very strong |   3_000_000|Age-737-year|Male  |Saiyan    |       175|        62|1      
#        ......+--------+            +------------+------------+      +          +----------+----------+...... 
#             2|Vegeta  |very strong |   2_000_000|Age-732-year|Male  |Saiyan    |       164|        56|2      
#        ......+--------+------------+------------+------------+      +----------+----------+----------+...... 
#             3|Piccolo |strong      |   1_000_000|Age-753-year|Male  |Namekian  |       226|       116|3      
#        ......+--------+------------+------------+------------+------+----------+----------+----------+...... 
#             4|Bulma   |very weak   |           3|Age-733-year|Female|Earthling |       165|        49|4      
#        ......+--------+------------+------------+------------+------+          +----------+----------+...... 
#             5|Krillin |good        |      75_000|Age-736-year|Male  |Earthling |       153|        45|5      
#        ......+--------+------------+------------+------------+      +          +----------+----------+...... 
#             6|Yamcha  |weak        |       1_480|Age-733-year|Male  |Earthling |       183|        68|6      
#        ......+--------+------------+------------+------------+------+----------+----------+----------+...... 
#         index:0       :1           :2           :3           :4     :5         :6         :7         :index
#       
#       
#       #print_idx2_borderプロパティで枠の種類を変えられる
#       >>> c.print_idx2_border = 'Index_simple'
#       >>> c.print_idx2()
#         index 0        1            2            3            4      5          6          7          index  
#               -------- ------------ ------------ ------------ ------ ---------- ---------- ----------        
#             0|Name     Strength     Buttle Power Birthdate    Sex    Race       Height(cm) Weight(kg)|0      
#             1|Goku     very strong     3_000_000 Age-737-year Male   Saiyan            175         62|1      
#             2|Vegeta   very strong     2_000_000 Age-732-year Male   Saiyan            164         56|2      
#             3|Piccolo  strong          1_000_000 Age-753-year Male   Namekian          226        116|3      
#             4|Bulma    very weak               3 Age-733-year Female Earthling         165         49|4      
#             5|Krillin  good               75_000 Age-736-year Male   Earthling         153         45|5      
#             6|Yamcha   weak                1_480 Age-733-year Male   Earthling         183         68|6      
#               -------- ------------ ------------ ------------ ------ ---------- ---------- ----------        
#         index 0        1            2            3            4      5          6          7          index
#       
#       
#       #printメソッドでデータを確認しヘッダーとデータ範囲を設定する
#       #ヘッダーとデータ範囲を設定すると編集や集計操作が簡単にできるようになる
#       #
#       #   header_idxプロパティにヘッダーのインデックスを設定する
#       #   data_row_rangeプロパティにヘッダー＆フッターを含まないデータ範囲をsliceで設定する
#       #
#       >>> c.header_idx = 0 #ヘッダーのインデックスを設定
#       >>> c.data_row_range = slice(1, None) #データ範囲を設定
#       >>>
#       >>> c.get_header()
#       ['Name', 'Strength', 'Buttle Power', 'Birthdate', 'Sex', 'Race', 'Height(cm)', 'Weight(kg)']
#       >>> c.get_header_idx('Race')
#       5
#       >>> c.get_header_value(5)
#       'Race'
#       >>>
#
#       >>> c['Race'] #TwoDimArrayインスタンスのインデクシングからもget_header_idxメソッドを呼び出せる
#       5
#       >>>
#
#
#       #TwoDimArrayへの問い合わせが可能
#       >>> c.inquire_field_value('Goku', 'Sex') #孫悟空の性別は？
#       'Male'
#       >>> c.inquire_field_value('Male', 'Height(cm)') #男の身長は？
#       [175, 164, 226, 153, 183]
#       >>>
#
#
#       #TwoDimArrayのフィールド情報の取得、インデックスの確認が可能
#       >>> c.get_field_value(3, 0)
#       'Piccolo'
#       >>> 
#       >>> c.get_field_idx('Earthling') #行列全体から検索
#       (4, 5)
#       >>> c.get_field_idx('Earthling', slice(5, None), slice(5, 6)) #行列範囲を絞って検索
#       (5, 5)
#       >>> c.get_field_idx_all('Earthling') #地球人を全て検索
#       [(4, 5), (5, 5), (6, 5)]
#       >>>
#
#       >>> c('Earthling') #TwoDimArrayインスタンスのインスタンス呼び出しからもget_field_idxメソッドを呼び出せる
#       (4, 5)
#       >>>
#
#
#       #インデックス5の列を削除
#       >>> c.del_column(5)
#       >>> print(c)
#       Name   , Strength   , Buttle Power, Birthdate   , Sex   , Height(cm), Weight(kg)
#       Goku   , very strong,    3_000_000, Age-737-year, Male  ,        175,         62
#       Vegeta , very strong,    2_000_000, Age-732-year, Male  ,        164,         56
#       Piccolo, strong     ,    1_000_000, Age-753-year, Male  ,        226,        116
#       Bulma  , very weak  ,            3, Age-733-year, Female,        165,         49
#       ↓(There are 2 rows)
#       
#
#       #インデックス1～3の範囲内の列を削除(インデックス1と2の列を削除)
#       >>> c.del_column(slice(1, 3))
#       >>> print(c)
#       Name   , Birthdate   , Sex   , Height(cm), Weight(kg)
#       Goku   , Age-737-year, Male  ,        175,         62
#       Vegeta , Age-732-year, Male  ,        164,         56
#       Piccolo, Age-753-year, Male  ,        226,        116
#       Bulma  , Age-733-year, Female,        165,         49
#       ↓(There are 2 rows)
#       
#
#       #インデックス1の列とインデックス2の列を入れ替える
#       >>> c.chg_colidx(1, 2)
#       >>> print(c)
#       Name   , Sex   , Birthdate   , Height(cm), Weight(kg)
#       Goku   , Male  , Age-737-year,        175,         62
#       Vegeta , Male  , Age-732-year,        164,         56
#       Piccolo, Male  , Age-753-year,        226,        116
#       Bulma  , Female, Age-733-year,        165,         49
#       ↓(There are 2 rows)
#       
#
#       #TwoDimArrayの生データはdataの中に入っているので直接編集可能
#       #(列操作用のメソッドは用意してあるが、基本的な行操作は簡単な配列操作で行えるので直接dataを操作する)
#       #
#       >>> c.data
#       [['Name', 'Sex', 'Birthdate', 'Height(cm)', 'Weight(kg)'], ['Goku', 'Male', 'Age-737-year', 175, 62], ['Vegeta', 'Male', 'Age-732-year', 164, 56], ['Piccolo', 'Male', 'Age-753-year', 226, 116], ['Bulma', 'Female', 'Age-733-year', 165, 49], ['Krillin', 'Male', 'Age-736-year', 153, 45], ['Yamcha', 'Male', 'Age-733-year', 183, 68]]
#       >>>
#
#
#       #TwoDimArrayにデータ追加(csv.str2list関数は文字列を配列に変換する)
#       >>> c.data.append(csv.str2list('Trunks, Male, Age-766-year, 170, 60'))
#       >>> c.print()
#       Name   , Sex   , Birthdate   , Height(cm), Weight(kg)
#       Goku   , Male  , Age-737-year,        175,         62
#       Vegeta , Male  , Age-732-year,        164,         56
#       Piccolo, Male  , Age-753-year,        226,        116
#       Bulma  , Female, Age-733-year,        165,         49
#       Krillin, Male  , Age-736-year,        153,         45
#       Yamcha , Male  , Age-733-year,        183,         68
#       Trunks , Male  , Age-766-year,        170,         60
#       
#
#       #インデックス0に列[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]を追加
#       >>> c.add_column(0, [i for i in range(10)])
#       >>> c.print()
#       0, Name   , Sex   , Birthdate   , Height(cm), Weight(kg)
#       1, Goku   , Male  , Age-737-year,        175,         62
#       2, Vegeta , Male  , Age-732-year,        164,         56
#       3, Piccolo, Male  , Age-753-year,        226,        116
#       4, Bulma  , Female, Age-733-year,        165,         49
#       5, Krillin, Male  , Age-736-year,        153,         45
#       6, Yamcha , Male  , Age-733-year,        183,         68
#       7, Trunks , Male  , Age-766-year,        170,         60
#       8,        ,       ,             ,           ,           
#       9,        ,       ,             ,           ,           
#       
#
#       #身長と体重からBMI係数を算出し、TwoDimArrayの最後尾に追加
#       #
#       #   cal_columnsメソッドの引数:
#       #       計算に必要なデータ(身長、体重)がある列の指定(4,5)、
#       #       BMIを計算する関数(lambda h,w: int(w/(h/100)/(h/100)))、
#       #
#       >>> bmi = c.cal_columns((4,5), lambda h,w: int(w/(h/100)/(h/100)))
#       >>> bmi
#       ['', 20, 20, 22, 17, 19, 20, 20, '', '']
#       >>> bmi[0] = 'BMI'
#       >>> c.add_column(None, bmi)
#       >>> print(c)
#       0, Name   , Sex   , Birthdate   , Height(cm), Weight(kg), BMI
#       1, Goku   , Male  , Age-737-year,        175,         62,  20
#       2, Vegeta , Male  , Age-732-year,        164,         56,  20
#       3, Piccolo, Male  , Age-753-year,        226,        116,  22
#       4, Bulma  , Female, Age-733-year,        165,         49,  17
#       ↓(There are 5 rows)
#       
#
#       #インデックス1～8の範囲内の行をBMI係数でsort
#       #
#       #   c.sort(lambda row: row[c['BMI']], True)だとデータ範囲[20, 20, 22, 17, 19, 20, 20, '', '']を
#       #   sortすることになり、数字と文字の異なるタイプのsortはできないのでエラーになる
#       #
#       #   エラーを回避するために２つの方法がある
#       #       1. c.data_row_range=slice(1,8)として全体のデータ範囲を変更する
#       #       2. sortメソッドでsortする際のデータ範囲を指定(row_start_idx=1, row_end_idx=8)する
#       #
#       >>> c.sort(lambda row: row[c['BMI']], reverse=True, row_start_idx=1, row_end_idx=8) #c['BMI'] == 6
#       >>> c.print()
#       0, Name   , Sex   , Birthdate   , Height(cm), Weight(kg), BMI
#       3, Piccolo, Male  , Age-753-year,        226,        116,  22
#       1, Goku   , Male  , Age-737-year,        175,         62,  20
#       2, Vegeta , Male  , Age-732-year,        164,         56,  20
#       6, Yamcha , Male  , Age-733-year,        183,         68,  20
#       7, Trunks , Male  , Age-766-year,        170,         60,  20
#       5, Krillin, Male  , Age-736-year,        153,         45,  19
#       4, Bulma  , Female, Age-733-year,        165,         49,  17
#       8,        ,       ,             ,           ,           ,    
#       9,        ,       ,             ,           ,           ,    
#       
#
#       #フィールド値の変換(男と女を記号表記に変換)
#       >>> c.replace_field('Male', 'M')
#       >>> c.replace_field('Female', 'F')
#       >>> c.print()
#       0, Name   , Sex, Birthdate   , Height(cm), Weight(kg), BMI
#       3, Piccolo, M  , Age-753-year,        226,        116,  22
#       1, Goku   , M  , Age-737-year,        175,         62,  20
#       2, Vegeta , M  , Age-732-year,        164,         56,  20
#       6, Yamcha , M  , Age-733-year,        183,         68,  20
#       7, Trunks , M  , Age-766-year,        170,         60,  20
#       5, Krillin, M  , Age-736-year,        153,         45,  19
#       4, Bulma  , F  , Age-733-year,        165,         49,  17
#       8,        ,    ,             ,           ,           ,    
#       9,        ,    ,             ,           ,           ,    
#       
#       
#       #フィールド値を正規表現で変換
#       >>> chg_year = c.resub_field(r'Age-(\d+)-year', r'Age \1')
#       >>> print(chg_year)
#       0, Name   , Sex, Birthdate, Height(cm), Weight(kg), BMI
#       3, Piccolo, M  , Age 753  ,        226,        116,  22
#       1, Goku   , M  , Age 737  ,        175,         62,  20
#       2, Vegeta , M  , Age 732  ,        164,         56,  20
#       6, Yamcha , M  , Age 733  ,        183,         68,  20
#       ↓(There are 5 rows)
#       
#
#       #男だけを抽出
#       >>> man = chg_year.filter(lambda row: row[c['Sex']]=='M') #c['Sex'] == 2
#       >>> man.print()
#       0, Name   , Sex, Birthdate, Height(cm), Weight(kg), BMI
#       3, Piccolo, M  , Age 753  ,        226,        116,  22
#       1, Goku   , M  , Age 737  ,        175,         62,  20
#       2, Vegeta , M  , Age 732  ,        164,         56,  20
#       6, Yamcha , M  , Age 733  ,        183,         68,  20
#       7, Trunks , M  , Age 766  ,        170,         60,  20
#       5, Krillin, M  , Age 736  ,        153,         45,  19
#       
#
#       #インデックス0の列を列['No.', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]に置き換える
#       >>> man.chg_column(0, ['No.', *[i for i in range(1, 10)]])
#       >>> man.print()
#       No., Name   , Sex, Birthdate, Height(cm), Weight(kg), BMI
#         1, Piccolo, M  , Age 753  ,        226,        116,  22
#         2, Goku   , M  , Age 737  ,        175,         62,  20
#         3, Vegeta , M  , Age 732  ,        164,         56,  20
#         4, Yamcha , M  , Age 733  ,        183,         68,  20
#         5, Trunks , M  , Age 766  ,        170,         60,  20
#         6, Krillin, M  , Age 736  ,        153,         45,  19
#         7,        ,    ,          ,           ,           ,    
#         8,        ,    ,          ,           ,           ,    
#         9,        ,    ,          ,           ,           ,    
#       
#
#       #インデックス2～4の範囲内の列を取り出す
#       >>> sex_birthdate = man.remove_column(slice(2,4))
#       >>> sex_birthdate
#       [['Sex', 'M', 'M', 'M', 'M', 'M', 'M', '', '', ''], ['Birthdate', 'Age 753', 'Age 737', 'Age 732', 'Age 733', 'Age 766', 'Age 736', '', '', '']]
#       >>> 
#       >>> print(man)
#       No., Name   , Height(cm), Weight(kg), BMI
#         1, Piccolo,        226,        116,  22
#         2, Goku   ,        175,         62,  20
#         3, Vegeta ,        164,         56,  20
#         4, Yamcha ,        183,         68,  20
#       ↓(There are 5 rows)
#       
#
#       #取り出した列をTwoDimArrayの最後尾に追加
#       >>> man.extend_columns(None, sex_birthdate)
#       >>> man.print()
#       No., Name   , Height(cm), Weight(kg), BMI, Sex, Birthdate
#         1, Piccolo,        226,        116,  22, M  , Age 753  
#         2, Goku   ,        175,         62,  20, M  , Age 737  
#         3, Vegeta ,        164,         56,  20, M  , Age 732  
#         4, Yamcha ,        183,         68,  20, M  , Age 733  
#         5, Trunks ,        170,         60,  20, M  , Age 766  
#         6, Krillin,        153,         45,  19, M  , Age 736  
#         7,        ,           ,           ,    ,    ,          
#         8,        ,           ,           ,    ,    ,          
#         9,        ,           ,           ,    ,    ,          
#       
#
#       #TwoDimArrayを枠で囲む
#       #枠の種類(border_pattern)はchk_border関数で確認できる(例ではborder_pattern='Grid'を選択している)
#       #
#       >>> man2 = man.wrap_border('Grid')
#       >>> man2.print()
#       +----+--------+----------+----------+----+----+----------+
#       |No. |Name    |Height(cm)|Weight(kg)|BMI |Sex |Birthdate |
#       +====+========+==========+==========+====+====+==========+
#       |   1|Piccolo |       226|       116|  22|M   |Age 753   |
#       +----+--------+----------+----------+----+    +----------+
#       |   2|Goku    |       175|        62|  20|M   |Age 737   |
#       +----+--------+----------+----------+    +    +----------+
#       |   3|Vegeta  |       164|        56|  20|M   |Age 732   |
#       +----+--------+----------+----------+    +    +----------+
#       |   4|Yamcha  |       183|        68|  20|M   |Age 733   |
#       +----+--------+----------+----------+    +    +----------+
#       |   5|Trunks  |       170|        60|  20|M   |Age 766   |
#       +----+--------+----------+----------+----+    +----------+
#       |   6|Krillin |       153|        45|  19|M   |Age 736   |
#       +----+--------+----------+----------+----+----+----------+
#       |   7|                                                   |
#       +----+        +          +          +    +    +          +
#       |   8|                                                   |
#       +----+        +          +          +    +    +          +
#       |   9|                                                   |
#       +----+--------+----------+----------+----+----+----------+
#       
#       
#       #各列の表示書式フォーマットをカスタマイズできる
#       #
#       #   ヘッダー: インデックス0の列は右詰め、それ以外は中央寄せ
#       #   データー: インデックス4の列は左詰め、それ以外は右詰め
#       #   文字幅: インデックス5の文字幅は5、それ以外は10
#       #
#       #   ※枠で囲んだ後は調整できないのでprint_chg_formatメソッドで調整＆確認後wrap_borderメソッドで囲む
#       #
#       >>> man.print_chg_format(header_aligns={0:'>', None:'^'}, aligns={4:'<', None:'>'}, widths={5:5, None:10})
#              No.,    Name   , Height(cm), Weight(kg),    BMI    ,  Sex , Birthdate 
#                1,    Piccolo,        226,        116, 22        ,     M,    Age 753
#                2,       Goku,        175,         62, 20        ,     M,    Age 737
#                3,     Vegeta,        164,         56, 20        ,     M,    Age 732
#                4,     Yamcha,        183,         68, 20        ,     M,    Age 733
#                5,     Trunks,        170,         60, 20        ,     M,    Age 766
#                6,    Krillin,        153,         45, 19        ,     M,    Age 736
#                7,           ,           ,           ,           ,      ,           
#                8,           ,           ,           ,           ,      ,           
#                9,           ,           ,           ,           ,      ,           
#
#       >>> man3 = man.wrap_border('Grid', header_aligns={0:'>', None:'^'}, aligns={4:'<', None:'>'}, widths={5:5, None:10})
#       >>> man3.print()
#       +----------+----------+----------+----------+----------+------+----------+
#       |       No.|   Name   |Height(cm)|Weight(kg)|   BMI    | Sex  |Birthdate |
#       +==========+==========+==========+==========+==========+======+==========+
#       |         1|   Piccolo|       226|       116|22        |     M|   Age 753|
#       +----------+----------+----------+----------+----------+      +----------+
#       |         2|      Goku|       175|        62|20        |     M|   Age 737|
#       +----------+----------+----------+----------+          +      +----------+
#       |         3|    Vegeta|       164|        56|20        |     M|   Age 732|
#       +----------+----------+----------+----------+          +      +----------+
#       |         4|    Yamcha|       183|        68|20        |     M|   Age 733|
#       +----------+----------+----------+----------+          +      +----------+
#       |         5|    Trunks|       170|        60|20        |     M|   Age 766|
#       +----------+----------+----------+----------+----------+      +----------+
#       |         6|   Krillin|       153|        45|19        |     M|   Age 736|
#       +----------+----------+----------+----------+----------+------+----------+
#       |         7|                                                             |
#       +----------+          +          +          +          +      +          +
#       |         8|                                                             |
#       +----------+          +          +          +          +      +          +
#       |         9|                                                             |
#       +----------+----------+----------+----------+----------+------+----------+
#       
#
#       #TwoDimArrayをsample2.csvファイルに保存
#       >>> man.save('sample2.csv', encoding='utf8')
#
#
#       #TwoDimArrayをsample2.csvファイルに追加保存
#       >>> man3.save('sample2.csv', mode='a', encoding='utf8')
#
#
#----------------------------------------------------------------------------------------------------
#       #文字列から簡単にTwoDimArrayを作成できる
#       #フィールドを複数行で表示するmultiple-lines表示が可能
#       #
#       #   multiple-linesのデリミタはr'\n' == '\\n'
#       #   multiple_lines_delimiterプロパティで変更可能
#       #
#       >>> z = csv.csv2tda("""
#       Name, Born, Occupation
#       Graham\\nArthur\\nChapman, 1941, Comedian\\nwriter\\nactor
#       John\\nMarwood\\nCleese, 1939, Actor\\nvoice actor\\ncomedian\\nscreenwriter\\nproducer
#       Michael\\nEdward\\nPalin, 1943, Actor\\nwriter\\ntelevision\\npresenter\\ncomedian
#       """)
#       >>> 
#       >>> z.trim() #空の行、空の列を削除
#       >>> z.header_idx = 0 #ヘッダーのインデックスを設定
#       >>> z.data_row_range = slice(1, None) #データ範囲を設定
#       >>> z.print2()
#       +--------+------+------------+
#       |Name    |Born  |Occupation  |
#       +--------+------+------------+
#       |Graham  | 1_941|Comedian    |
#       |Arthur  |      |writer      |
#       |Chapman |      |actor       |
#       +--------+------+------------+
#       |John    | 1_939|Actor       |
#       |Marwood |      |voice actor |
#       |Cleese  |      |comedian    |
#       |        |      |screenwriter|
#       |        |      |producer    |
#       +--------+------+------------+
#       |Michael | 1_943|Actor       |
#       |Edward  |      |writer      |
#       |Palin   |      |television  |
#       |        |      |presenter   |
#       |        |      |comedian    |
#       +--------+------+------------+
#       >>> 
#       >>> z.print_idx2()
#         index:0       :1     :2           :index  
#        ......+--------+------+------------+...... 
#             0|Name    |Born  |Occupation  |0      
#        ......+--------+------+------------+...... 
#             1|Graham  | 1_941|Comedian    |1      
#              |Arthur  |      |writer      |       
#              |Chapman |      |actor       |       
#        ......+--------+------+------------+...... 
#             2|John    | 1_939|Actor       |2      
#              |Marwood |      |voice actor |       
#              |Cleese  |      |comedian    |       
#              |        |      |screenwriter|       
#              |        |      |producer    |       
#        ......+--------+------+------------+...... 
#             3|Michael | 1_943|Actor       |3      
#              |Edward  |      |writer      |       
#              |Palin   |      |television  |       
#              |        |      |presenter   |       
#              |        |      |comedian    |       
#        ......+--------+------+------------+...... 
#         index:0       :1     :2           :index
#       >>>
#       >>> z.multiple_lines = False #multiple_linesプロパティでmultiple-lines表示を切り替えられる
#       >>> z.print2()
#       +------------------------+------+----------------------------------------------------+
#       |Name                    |Born  |Occupation                                          |
#       +------------------------+------+----------------------------------------------------+
#       |Graham\nArthur\nChapman | 1_941|Comedian\nwriter\nactor                             |
#       +------------------------+------+----------------------------------------------------+
#       |John\nMarwood\nCleese   | 1_939|Actor\nvoice actor\ncomedian\nscreenwriter\nproducer|
#       +------------------------+------+----------------------------------------------------+
#       |Michael\nEdward\nPalin  | 1_943|Actor\nwriter\ntelevision\npresenter\ncomedian      |
#       +------------------------+------+----------------------------------------------------+
#       
#       
#       >>> t = csv.csv2tda("""
#       hoge, fuga, HOGE, FUGA
#       a,b,c,d
#       123,12345,1234567,123456789
#       """)
#       >>> 
#       >>> t.trim() #空の行、空の列を削除
#       >>> t.print()
#       hoge, fuga  , HOGE     , FUGA       
#       a   , b     , c        , d          
#        123, 12_345, 1_234_567, 123_456_789
#       
#
#       #列のインデックスを指定してTwoDimArrayを再構築できる
#       >>> t = t.arrange_columns(3,2,1,0)
#       >>> t.print()
#       FUGA       , HOGE     , fuga  , hoge
#       d          , c        , b     , a   
#       123_456_789, 1_234_567, 12_345,  123
#       
#       
#       #行のインデックスを指定してTwoDimArrayを再構築できる
#       >>> t = t.arrange_rows(1,0,2)
#       >>> t.print()
#       d          , c        , b     , a   
#       FUGA       , HOGE     , fuga  , hoge
#       123_456_789, 1_234_567, 12_345,  123
#       
#
#----------------------------------------------------------------------------------------------------
#       #fillメソッド、map_fieldメソッド、research_field、tda2list、counter_columnメソッドの使用例
#       #2次元配列からTwoDimArray作成
#       #
#       >>> m = csv.TwoDimArray([[1],[1,2],[1,2,3],[1,2,3,4],[1,2,3],[1,2],[1]])
#       >>> m.print()
#       1
#       1, 2
#       1, 2, 3
#       1, 2, 3, 4
#       1, 2, 3
#       1, 2
#       1
#       
#       
#       #行列の欠けている箇所をゼロで埋める
#       >>> m.fill(0)
#       >>> m.print()
#       1, 0, 0, 0
#       1, 2, 0, 0
#       1, 2, 3, 0
#       1, 2, 3, 4
#       1, 2, 3, 0
#       1, 2, 0, 0
#       1, 0, 0, 0
#       
#       
#       #インデックス2～5の範囲内の行のフィールド値を2倍にする
#       >>> m2 = m.map_field(lambda field: field*2, 2, 5)
#       >>> m2.print()
#       1, 0, 0, 0
#       1, 2, 0, 0
#       2, 4, 6, 0
#       2, 4, 6, 8
#       2, 4, 6, 0
#       1, 2, 0, 0
#       1, 0, 0, 0
#       
#       
#       #2、4、6で構成されたフィールドだけを抽出する
#       >>> m3 = m2.research_field(r'[246]')
#       >>> m3.print()
#        ,  ,  , 
#        , 2,  , 
#       2, 4, 6, 
#       2, 4, 6, 
#       2, 4, 6, 
#        , 2,  , 
#        ,  ,  , 
#       
#       
#       #4列のデータを6列に変更する
#       >>> m4 = csv.list2tda(m2.tda2list(), 6)
#       >>> m4.print()
#       1, 0, 0, 0, 1, 2
#       0, 0, 2, 4, 6, 0
#       2, 4, 6, 8, 2, 4
#       6, 0, 1, 2, 0, 0
#       1, 0, 0, 0
#       
#       
#       #インデックス0の列のフィールド値をカウント
#       >>> m4.counter_column(0)
#       Counter({1: 2, 0: 1, 2: 1, 6: 1})
#       
#       
#----------------------------------------------------------------------------------------------------
#       #辞書からTwoDimArrayを作成することも可能
#       #
#       #   辞書の各アイテムは列となる
#       #
#       >>> import numpy as np
#       >>> 
#       >>> d= {'NAME': list('ABCDEFG'), 'VALUE_1': np.random.randn(7), 'VALUE_2': np.random.randn(7)}
#       >>> h = csv.dict2tda(d)
#       >>> h.print()
#       NAME, VALUE_1, VALUE_2
#       A   ,    0.40,    1.63
#       B   ,   -1.37,    0.64
#       C   ,   -0.06,    0.87
#       D   ,    0.44,    0.73
#       E   ,   -1.30,   -1.11
#       F   ,   -1.73,    0.17
#       G   ,   -0.82,   -0.94
#       
#       
#       #floatの精度(小数点以下の桁数)を調整可能
#       >>> h.precision = 10
#       >>> h.print()
#       NAME, VALUE_1      , VALUE_2      
#       A   ,  0.4003742639,  1.6272049722
#       B   , -1.3694450047,  0.6399934786
#       C   , -0.0633841457,  0.8659692839
#       D   ,  0.4384958907,  0.7319732920
#       E   , -1.2958969709, -1.1108404649
#       F   , -1.7329270126,  0.1683664238
#       G   , -0.8177787733, -0.9438108092
#       
#       >>> h.print2()
#       +----+--------------+--------------+
#       |NAME|VALUE_1       |VALUE_2       |
#       +----+--------------+--------------+
#       |A   |  0.4003742639|  1.6272049722|
#       +----+--------------+--------------+
#       |B   | -1.3694450047|  0.6399934786|
#       +----+--------------+--------------+
#       |C   | -0.0633841457|  0.8659692839|
#       +----+--------------+--------------+
#       |D   |  0.4384958907|  0.7319732920|
#       +----+--------------+--------------+
#       |E   | -1.2958969709| -1.1108404649|
#       +----+--------------+--------------+
#       |F   | -1.7329270126|  0.1683664238|
#       +----+--------------+--------------+
#       |G   | -0.8177787733| -0.9438108092|
#       +----+--------------+--------------+
#       
#       
#----------------------------------------------------------------------------------------------------
#       #データ集計の使用例
#       >>> c = csv.load('sample.csv', encoding='utf8')
#       >>> c.print2()
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Name    |Strength    |Buttle Power|Birthdate   |Sex   |Race      |Height(cm)|Weight(kg)|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Goku    |very strong |   3_000_000|Age-737-year|Male  |Saiyan    |       175|        62|
#       +--------+            +------------+------------+      +          +----------+----------+
#       |Vegeta  |very strong |   2_000_000|Age-732-year|Male  |Saiyan    |       164|        56|
#       +--------+------------+------------+------------+      +----------+----------+----------+
#       |Piccolo |strong      |   1_000_000|Age-753-year|Male  |Namekian  |       226|       116|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Bulma   |very weak   |           3|Age-733-year|Female|Earthling |       165|        49|
#       +--------+------------+------------+------------+------+          +----------+----------+
#       |Krillin |good        |      75_000|Age-736-year|Male  |Earthling |       153|        45|
#       +--------+------------+------------+------------+      +          +----------+----------+
#       |Yamcha  |weak        |       1_480|Age-733-year|Male  |Earthling |       183|        68|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       
#       
#       #ヘッダーのインデックスとデータ範囲を設定
#       >>> c.header_idx = 0
#       >>> c.data_row_range = slice(1, None)
#       
#       
#       #性別でグループ化して各グループの合計値を集計(sum関数で集計できないフィールド値は空になる)
#       >>> c.groupby(c['Sex'], func=sum).print2()
#       +------+----+--------+------------+----------+----+----------+----------+
#       |Sex   |Name|Strength|Buttle Power|Birthdate |Race|Height(cm)|Weight(kg)|
#       +------+----+--------+------------+----------+----+----------+----------+
#       |Male  |             |   6_076_480|               |       901|       347|
#       +------+    +        +------------+          +    +----------+----------+
#       |Female|             |           3|               |       165|        49|
#       +------+----+--------+------------+----------+----+----------+----------+
#       
#       
#       #集計対象を身長だけに限定
#       >>> c.groupby(c['Sex'], c['Height(cm)'], func=sum).print2()
#       +------+----------+
#       |Sex   |Height(cm)|
#       +------+----------+
#       |Male  |       901|
#       +------+----------+
#       |Female|       165|
#       +------+----------+
#       
#       
#       #性別と種族でグループ化し、集計対象は身長だけに限定
#       >>> c.groupby((c['Sex'], c['Race']), c['Height(cm)'], func=sum).print2()
#       +------+----------+----------+
#       |Sex   |Race      |Height(cm)|
#       +------+----------+----------+
#       |Male  |Saiyan    |       339|
#       +      +----------+----------+
#       |Male  |Namekian  |       226|
#       +------+----------+----------+
#       |Female|Earthling |       165|
#       +------+          +----------+
#       |Male  |Earthling |       336|
#       +------+----------+----------+
#       
#       
#       #男女別の身長と体重の平均値
#       >>> c.groupby(c['Sex'], (c['Height(cm)'], c['Weight(kg)']), func=csv.mean).print2()
#       +------+----------+----------+
#       |Sex   |Height(cm)|Weight(kg)|
#       +------+----------+----------+
#       |Male  |    180.20|     69.40|
#       +------+----------+----------+
#       |Female|       165|        49|
#       +------+----------+----------+
#       
#       
#       #同じ誕生日の人はいるのかな？
#       >>> c.groupby(c['Birthdate'], c['Name'], func=len).print2()
#       +------------+----+
#       |Birthdate   |Name|
#       +------------+----+
#       |Age-737-year|   1|
#       +------------+    +
#       |Age-732-year|   1|
#       +------------+    +
#       |Age-753-year|   1|
#       +------------+----+
#       |Age-733-year|   2|
#       +------------+----+
#       |Age-736-year|   1|
#       +------------+----+
#       
#       
#       #誰と誰が同じ誕生日なのかな？
#       #
#       #   func引数のデフォルト値はlambda fields: r'\n'.join(map(str, fields))となっているので
#       #   グループ化したフィールド値を並べるだけならば省略可能
#       #
#       >>> c.groupby(c['Birthdate'], c['Name']).print2()
#       +------------+--------+
#       |Birthdate   |Name    |
#       +------------+--------+
#       |Age-737-year|Goku    |
#       +------------+--------+
#       |Age-732-year|Vegeta  |
#       +------------+--------+
#       |Age-753-year|Piccolo |
#       +------------+--------+
#       |Age-733-year|Bulma   |
#       |            |Yamcha  |
#       +------------+--------+
#       |Age-736-year|Krillin |
#       +------------+--------+
#       >>> 
#       >>> c.groupby(c['Sex']).print2()
#       +------+--------+------------+------------+------------+----------+----------+----------+
#       |Sex   |Name    |Strength    |Buttle Power|Birthdate   |Race      |Height(cm)|Weight(kg)|
#       +------+--------+------------+------------+------------+----------+----------+----------+
#       |Male  |Goku    |very strong |   3_000_000|Age-737-year|Saiyan    |       175|        62|
#       |      |Vegeta  |very strong |   2_000_000|Age-732-year|Saiyan    |       164|        56|
#       |      |Piccolo |strong      |   1_000_000|Age-753-year|Namekian  |       226|       116|
#       |      |Krillin |good        |      75_000|Age-736-year|Earthling |       153|        45|
#       |      |Yamcha  |weak        |       1_480|Age-733-year|Earthling |       183|        68|
#       +------+--------+------------+------------+------------+----------+----------+----------+
#       |Female|Bulma   |very weak   |           3|Age-733-year|Earthling |       165|        49|
#       +------+--------+------------+------------+------------+----------+----------+----------+
#       
#       
#       #性別と種族でクロス集計
#       >>> c.cross_count(c['Race'], c['Sex']).print2()
#       +------+----------+--------+--------+
#       |      |Earthling |Namekian|Saiyan  |
#       +------+----------+--------+--------+
#       |Female|1 (17%)   |0 (0%)   0 (0%)  |
#       +------+----------+--------+--------+
#       |Male  |2 (33%)   |1 (17%) |2 (33%) |
#       +------+----------+--------+--------+
#       
#       
#       #field_fmt引数でフィールドの表示形式を設定できる
#       >>> c.cross_count(c['Race'], c['Sex'], field_fmt='{count}').print2()
#       +------+----------+--------+------+
#       |      |Earthling |Namekian|Saiyan|
#       +------+----------+--------+------+
#       |Female|         1|       0      0|
#       +------+----------+--------+------+
#       |Male  |         2|       1|     2|
#       +------+----------+--------+------+
#       
#       
#       #各列のデータ数、最大値、最小値、合計、平均、中央値、分散、標準偏差などを一度に確認できる
#       #
#       #   数字データのみが計算対象となり文字列は無視されるので、
#       #   文字列データだけで構成された列の計算結果は空白やゼロになる
#       #
#       >>> c.describe().print2()
#       +--------+----+--------+--------------------+----------+----+----+----------+----------+
#       |        |Name|Strength|Buttle Power        |Birthdate |Sex |Race|Height(cm)|Weight(kg)|
#       +--------+----+--------+--------------------+----------+----+----+----------+----------+
#       |len     |   0        0|                   6|         0    0    0|         6          6|
#       +--------+----+--------+--------------------+----------+----+----+----------+----------+
#       |max     |             |           3_000_000|                    |       226|       116|
#       +--------+    +        +--------------------+          +    +    +----------+----------+
#       |min     |             |                   3|                    |       153|        45|
#       +--------+----+--------+--------------------+----------+----+----+----------+----------+
#       |sum     |   0        0|           6_076_483|         0    0    0|     1_066|       396|
#       +--------+----+--------+--------------------+----------+----+----+----------+----------+
#       |mean    |             |        1_012_747.17|                    |    177.67|        66|
#       +--------+    +        +--------------------+          +    +    +----------+----------+
#       |median  |             |          537_500.00|                    |    170.00|     59.00|
#       +--------+    +        +--------------------+          +    +    +----------+----------+
#       |variance|             |1_570_337_249_772.17|                    |    665.47|       670|
#       +--------+    +        +--------------------+          +    +    +----------+----------+
#       |stdev   |             |        1_253_130.98|                    |     25.80|     25.88|
#       +--------+----+--------+--------------------+----------+----+----+----------+----------+
#       
#       
#       #グループ化したデータ(multiple-lines)の処理も可能
#       #
#       #   cal_columnsやmap_fieldメソッドなどはmultiple-linesの処理をサポートしている
#       #
#       >>> g = c.groupby(c['Sex'])
#       >>> g.print2()
#       +------+--------+------------+------------+------------+----------+----------+----------+
#       |Sex   |Name    |Strength    |Buttle Power|Birthdate   |Race      |Height(cm)|Weight(kg)|
#       +------+--------+------------+------------+------------+----------+----------+----------+
#       |Male  |Goku    |very strong |   3_000_000|Age-737-year|Saiyan    |       175|        62|
#       |      |Vegeta  |very strong |   2_000_000|Age-732-year|Saiyan    |       164|        56|
#       |      |Piccolo |strong      |   1_000_000|Age-753-year|Namekian  |       226|       116|
#       |      |Krillin |good        |      75_000|Age-736-year|Earthling |       153|        45|
#       |      |Yamcha  |weak        |       1_480|Age-733-year|Earthling |       183|        68|
#       +------+--------+------------+------------+------------+----------+----------+----------+
#       |Female|Bulma   |very weak   |           3|Age-733-year|Earthling |       165|        49|
#       +------+--------+------------+------------+------------+----------+----------+----------+
#       >>> 
#       >>> bmi = g.cal_columns((c['Height(cm)'], c['Weight(kg)']), lambda h,w: int(w/(h/100)/(h/100)))
#       >>> bmi
#       ['', '20\\n20\\n22\\n19\\n20', 17]
#       >>> bmi[0] = 'BMI'
#       >>> g.add_column(None, bmi)
#       >>> g.print2()
#       +------+--------+------------+------------+------------+----------+----------+----------+----+
#       |Sex   |Name    |Strength    |Buttle Power|Birthdate   |Race      |Height(cm)|Weight(kg)|BMI |
#       +------+--------+------------+------------+------------+----------+----------+----------+----+
#       |Male  |Goku    |very strong |   3_000_000|Age-737-year|Saiyan    |       175|        62|  20|
#       |      |Vegeta  |very strong |   2_000_000|Age-732-year|Saiyan    |       164|        56|  20|
#       |      |Piccolo |strong      |   1_000_000|Age-753-year|Namekian  |       226|       116|  22|
#       |      |Krillin |good        |      75_000|Age-736-year|Earthling |       153|        45|  19|
#       |      |Yamcha  |weak        |       1_480|Age-733-year|Earthling |       183|        68|  20|
#       +------+--------+------------+------------+------------+----------+----------+----------+----+
#       |Female|Bulma   |very weak   |           3|Age-733-year|Earthling |       165|        49|  17|
#       +------+--------+------------+------------+------------+----------+----------+----------+----+
#       
#       
#----------------------------------------------------------------------------------------------------
#       #print関連のメソッドに前後処理を簡単に追加可能
#       #
#       #   print_contextmanagerプロパティにcontextmanager用の関数を設定することで前後処理を簡単に追加できる
#       #
#       >>> n = csv.TwoDimArray([[i for i in range(1,j)] for j in range(2,7)])
#       >>> n.fill(0)
#       >>> n.print2()
#       +--+--+--+--+--+
#       | 1| 0  0  0  0|
#       +  +--+  +  +  +
#       | 1| 2| 0  0  0|
#       +  +  +--+  +  +
#       | 1| 2| 3| 0  0|
#       +  +  +  +--+  +
#       | 1| 2| 3| 4| 0|
#       +  +  +  +  +--+
#       | 1| 2| 3| 4| 5|
#       +--+--+--+--+--+
#       >>>
#       >>> def hoge(tda_self): #TwoDimArrayインスタンスを受け取る関数を定義する
#       	print('START')
#       	yield
#       	print('END')
#       
#       
#       >>> n.print_contextmanager = hoge
#       >>> n.print2()
#       START
#       +--+--+--+--+--+
#       | 1| 0  0  0  0|
#       +  +--+  +  +  +
#       | 1| 2| 0  0  0|
#       +  +  +--+  +  +
#       | 1| 2| 3| 0  0|
#       +  +  +  +--+  +
#       | 1| 2| 3| 4| 0|
#       +  +  +  +  +--+
#       | 1| 2| 3| 4| 5|
#       +--+--+--+--+--+
#       END
#       >>>
#
#
#       #print_contextmanagerプロパティに設定する関数はcsv.PrintContextManagerクラスに幾つか用意されている
#       >>> n.print_contextmanager = csv.PrintContextManager.aggregate(sum) #各行列の合計値を追加表示する
#       >>> n.print2()
#       +--+--+--+--+--+--+
#       | 1| 0  0  0  0| 1|
#       +  +--+  +  +  +--+
#       | 1| 2| 0  0  0| 3|
#       +  +  +--+  +  +--+
#       | 1| 2| 3| 0  0| 6|
#       +  +  +  +--+  +--+
#       | 1| 2| 3| 4| 0|10|
#       +  +  +  +  +--+--+
#       | 1| 2| 3| 4| 5|15|
#       +--+--+--+--+  +--+
#       | 5| 8| 9| 8| 5|35|
#       +--+--+--+--+--+--+
#       Add aggregate: sum
#       >>> n.data
#       [[1, 0, 0, 0, 0], [1, 2, 0, 0, 0], [1, 2, 3, 0, 0], [1, 2, 3, 4, 0], [1, 2, 3, 4, 5]] #データは元のまま
#       >>>
#
#
#       #各列の合計値を追加表示する
#       >>> n.print_contextmanager = csv.PrintContextManager.aggregate_col(sum)
#       >>> n.print2()
#       +--+--+--+--+--+
#       | 1| 0  0  0  0|
#       +  +--+  +  +  +
#       | 1| 2| 0  0  0|
#       +  +  +--+  +  +
#       | 1| 2| 3| 0  0|
#       +  +  +  +--+  +
#       | 1| 2| 3| 4| 0|
#       +  +  +  +  +--+
#       | 1| 2| 3| 4| 5|
#       +--+--+--+--+  +
#       | 5| 8| 9| 8| 5|
#       +--+--+--+--+--+
#       Add aggregate_col: sum
#       >>> n.data
#       [[1, 0, 0, 0, 0], [1, 2, 0, 0, 0], [1, 2, 3, 0, 0], [1, 2, 3, 4, 0], [1, 2, 3, 4, 5]] #データは元のまま
#       >>>
#       >>> n.data_row_range = slice(1, -1) #データ範囲を変更(最初と最後の行は無視される)
#       >>> n.print2()
#       +--+--+--+--+--+
#       | 1| 0  0  0  0|
#       +  +--+  +  +  +
#       | 1| 2| 0  0  0|
#       +  +  +--+  +  +
#       | 1| 2| 3| 0  0|
#       +  +  +  +--+  +
#       | 1| 2| 3| 4| 0|
#       +  +  +  +  +--+
#       | 1| 2| 3| 4| 5|
#       +--+--+--+  +--+
#       | 3| 6  6| 4| 0|
#       +--+--+--+--+--+
#       Add aggregate_col: sum
#       >>>
#       >>> n.print_contextmanager = None #Noneで無効化
#       >>> n.print2()
#       +--+--+--+--+--+
#       | 1| 0  0  0  0|
#       +  +--+  +  +  +
#       | 1| 2| 0  0  0|
#       +  +  +--+  +  +
#       | 1| 2| 3| 0  0|
#       +  +  +  +--+  +
#       | 1| 2| 3| 4| 0|
#       +  +  +  +  +--+
#       | 1| 2| 3| 4| 5|
#       +--+--+--+--+--+
#       
#       
#----------------------------------------------------------------------------------------------------
#       #欠損データを気にせずに集計が可能
#       #
#       #   データ内にブランク行があったり、一部のデータが欠けている場合は集計の邪魔になるためデータを整える必要があった
#       #   この問題を解決するために集計関数を「目的のデータだけ受け取るラッパー関数にする」機能が用意されている
#       #
#       >>> n = csv.TwoDimArray([[i for i in range(1,j)] for j in range(2,7)])
#       >>> n.fill()
#       >>> n.print2() #欠損データ(空フィールド)がある
#       +--+--+--+--+--+
#       | 1|           |
#       +  +--+  +  +  +
#       | 1| 2|        |
#       +  +  +--+  +  +
#       | 1| 2| 3|     |
#       +  +  +  +--+  +
#       | 1| 2| 3| 4|  |
#       +  +  +  +  +--+
#       | 1| 2| 3| 4| 5|
#       +--+--+--+--+--+
#       >>> 
#       >>> n.print_contextmanager = csv.PrintContextManager.aggregate(sum)
#       >>> n.print2() #合計値を集計できるのは欠損データが無い行列だけ
#       +--+--+--+--+--+--+
#       | 1|              |
#       +  +--+  +  +  +  +
#       | 1| 2|           |
#       +  +  +--+  +  +  +
#       | 1| 2| 3|        |
#       +  +  +  +--+  +  +
#       | 1| 2| 3| 4|     |
#       +  +  +  +  +--+--+
#       | 1| 2| 3| 4| 5|15|
#       +--+--+--+--+--+--+
#       | 5|              |
#       +--+--+--+--+--+--+
#       Add aggregate: sum
#
#
#       #csv.Wrapper.arg_of_numlistで集計関数sumをラップして数字だけが渡るようにする
#       >>> sum_nums = csv.Wrapper.arg_of_numlist(sum)
#       >>> n.print_contextmanager = csv.PrintContextManager.aggregate(sum_nums)
#       >>> n.print2() #空データが無視されて各行列の合計値を集計できる
#       +--+--+--+--+--+--+
#       | 1|           | 1|
#       +  +--+  +  +  +--+
#       | 1| 2|        | 3|
#       +  +  +--+  +  +--+
#       | 1| 2| 3|     | 6|
#       +  +  +  +--+  +--+
#       | 1| 2| 3| 4|  |10|
#       +  +  +  +  +--+--+
#       | 1| 2| 3| 4| 5|15|
#       +--+--+--+--+  +--+
#       | 5| 8| 9| 8| 5|35|
#       +--+--+--+--+--+--+
#       Add aggregate: sum
#       
#       
#----------------------------------------------------------------------------------------------------
#       #TwoDimArrayの回転
#       #
#       #   TwoDimArrayを左右に45度、90度毎に回転させるメソッドが用意されている
#       #   rotate_l45, rotate_r45, rotate_l90, rotate_r90
#       #
#       >>> r = csv.TwoDimArray([[1,2,3], [4,5,6], [7,8,9]])
#       >>> r.border_grouping = False
#       >>> r.print2()
#       +--+--+--+
#       | 1| 2| 3|
#       +--+--+--+
#       | 4| 5| 6|
#       +--+--+--+
#       | 7| 8| 9|
#       +--+--+--+
#       >>> 
#       >>> r.rotate_r45(); r.print2()
#       +--+--+--+--+--+
#       |  |  | 1|  |  |
#       +--+--+--+--+--+
#       |  | 4|  | 2|  |
#       +--+--+--+--+--+
#       | 7|  | 5|  | 3|
#       +--+--+--+--+--+
#       |  | 8|  | 6|  |
#       +--+--+--+--+--+
#       |  |  | 9|  |  |
#       +--+--+--+--+--+
#       >>> r.rotate_r45(); r.print2()
#       +--+--+--+
#       | 7| 4| 1|
#       +--+--+--+
#       | 8| 5| 2|
#       +--+--+--+
#       | 9| 6| 3|
#       +--+--+--+
#       
#       
#----------------------------------------------------------------------------------------------------
#       #TwoDimArrayの表示を他のアプリケーションで行う
#       #
#       #   IDLEやターミナルなどは横スクロール機能が無いため、csvの列データが多すぎると表示が折り返されて正常に表示できない
#       #   この問題を解決するために、print関連のメソッドの出力をファイルに保存する機能が用意されている
#       #   このファイルを横スクロールやズームなどの機能を備えたアプリケーションで開いておけば
#       #   ファイルの更新のたびにアプリケーションの表示を更新するだけでTwoDimArrayを確認できる
#       #
#       #   set_print_fileメソッドでprint関連のメソッドの出力を保存するファイルを指定する
#       #   set_print_fileメソッドを呼び出すと設定したファイルが関連付けされたアプリケーションで開く(Windowsのみ)
#       #   htmlファイルならブラウザが、txtファイルならエディタでファイルが開く(Windows以外は手動で開く必要がある)
#       #   (txtファイルの場合は外部からの更新を検出できるエディタを使用するのが望ましい
#       #    メモ帳だと外部からの更新を検出できないため閉じてから開きなおす必要がある)
#       #
#       >>> c = csv.load('sample.csv', encoding='utf8')
#       >>> c.header_idx = 0
#       >>> c.data_row_range = slice(1, None)
#       >>> c.set_print_file('_tmp.html', encoding='utf8') #拡張子がhtmlなので、Windowsの場合は既定ブラウザが起動してファイルが開く
#       >>> c.print2() #出力は設定したファイル(_tmp.html)に上書き保存されるのでブラウザを更新すれば新しいデータがすぐに見れる
#       >>>
#       >>> c.sort(lambda row:row[c['Sex']]) #加工して
#       >>> c.print2() #ファイルに出力して、ブラウザを更新して確認
#       >>>
#       >>> c.set_print_file() #引数無しでset_print_fileメソッドを呼べば設定が解除される
#       >>> c.print2()
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Name    |Strength    |Buttle Power|Birthdate   |Sex   |Race      |Height(cm)|Weight(kg)|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Bulma   |very weak   |           3|Age-733-year|Female|Earthling |       165|        49|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#       |Goku    |very strong |   3_000_000|Age-737-year|Male  |Saiyan    |       175|        62|
#       +--------+            +------------+------------+      +          +----------+----------+
#       |Vegeta  |very strong |   2_000_000|Age-732-year|Male  |Saiyan    |       164|        56|
#       +--------+------------+------------+------------+      +----------+----------+----------+
#       |Piccolo |strong      |   1_000_000|Age-753-year|Male  |Namekian  |       226|       116|
#       +--------+------------+------------+------------+      +----------+----------+----------+
#       |Krillin |good        |      75_000|Age-736-year|Male  |Earthling |       153|        45|
#       +--------+------------+------------+------------+      +          +----------+----------+
#       |Yamcha  |weak        |       1_480|Age-733-year|Male  |Earthling |       183|        68|
#       +--------+------------+------------+------------+------+----------+----------+----------+
#
#       
#----------------------------------------------------------------------------------------------------
#       #魔方陣の作成
#       #   任意のサイズの魔方陣を作成できる
#       #   作成した魔方陣はis_magicメソッドで縦・横・対角線の数字の合計を確認できる
#       #
#       >>>m = csv.Magic.magic(10)
#       >>>m.print2()
#       +--+--+--+--+--+--+--+--+--+----+
#       | 1|92|93| 7| 6| 5|94|98|99|  10|
#       +--+--+--+--+--+--+--+--+--+----+
#       |20|12|83|84|16|85|87|88|19|  11|
#       +--+--+--+--+--+--+--+--+--+----+
#       |30|29|23|74|75|76|77|28|22|  71|
#       +--+--+--+--+--+--+--+--+--+----+
#       |61|39|38|34|65|66|37|33|62|  70|
#       +--+--+--+--+--+--+--+--+--+----+
#       |51|52|48|47|45|46|44|53|59|  60|
#       +--+--+--+--+--+--+--+--+--+----+
#       |41|49|58|57|55|56|54|43|42|  50|
#       +--+--+--+--+--+--+--+--+--+----+
#       |40|69|68|64|35|36|67|63|32|  31|
#       +--+--+--+--+--+--+--+--+--+----+
#       |80|79|73|24|26|25|27|78|72|  21|
#       +--+--+--+--+--+--+--+--+--+----+
#       |90|82|13|17|86|15|14|18|89|  81|
#       +--+--+--+--+--+--+--+--+--+----+
#       |91| 2| 8|97|96|95| 4| 3| 9| 100|
#       +--+--+--+--+--+--+--+--+--+----+
#
#       #魔方陣の確認
#       >>>csv.Magic.is_magic(m.data)
#       natural_num : True
#       row_sum     : 505
#       col_sum     : 505
#       slash_sum   : 505
#       bslash_sum  : 505
#       True
#
#
#----------------------------------------------------------------------------------------------------
#       #pandasのDataFrameをTwoDimArrayに変換
#       #   TwoDimArrayのprint2関数で見やすくなる
#       #
#       >>>import pandas as pd
#       >>>df = pd.DataFrame({
#              '名前': ['佐藤', '斎藤', '鈴木', '田中'],
#              '年齢': [21, 30, 45, 16],
#              '住所': ['東京都', '岐阜県', '埼玉県', '大阪'],
#              '血液型': ['A', 'AB', 'O', 'O'],
#              'レベル': [6, 7, 5, 9],
#              'ポイント': [2900, 3400, 2500, 5100],
#          })
#       
#       >>>df
#          名前  年齢   住所 血液型  レベル  ポイント
#       0  佐藤  21  東京都   A    6  2900
#       1  斎藤  30  岐阜県  AB    7  3400
#       2  鈴木  45  埼玉県   O    5  2500
#       3  田中  16   大阪   O    9  5100
#       
#       >>>csv.df2tda(df).print2()
#       +----+----+------+------+------+--------+
#       |名前|年齢|住所  |血液型|レベル|ポイント|
#       +----+----+------+------+------+--------+
#       |佐藤|  21|東京都|A     |     6|   2_900|
#       +----+----+------+------+------+--------+
#       |斎藤|  30|岐阜県|AB    |     7|   3_400|
#       +----+----+------+------+------+--------+
#       |鈴木|  45|埼玉県|O     |     5|   2_500|
#       +----+----+------+      +------+--------+
#       |田中|  16|大阪  |O     |     9|   5_100|
#       +----+----+------+------+------+--------+
#       
#       >>>csv.df2tda(df, index=True).print2()
#       +--+----+----+------+------+------+--------+
#       |  |名前|年齢|住所  |血液型|レベル|ポイント|
#       +--+----+----+------+------+------+--------+
#       | 0|佐藤|  21|東京都|A     |     6|   2_900|
#       +--+----+----+------+------+------+--------+
#       | 1|斎藤|  30|岐阜県|AB    |     7|   3_400|
#       +--+----+----+------+------+------+--------+
#       | 2|鈴木|  45|埼玉県|O     |     5|   2_500|
#       +--+----+----+------+      +------+--------+
#       | 3|田中|  16|大阪  |O     |     9|   5_100|
#       +--+----+----+------+------+------+--------+
#       
#       
#----------------------------------------------------------------------------------------------------
__all__ = ['TwoDimArray', 'PrintContextManager', 'Wrapper', 'Magic', #class
           'load', 'csv2tda', 'df2tda', 'list2tda', 'dict2tda', 'str2list', 'list2str', 'row2column', 'chk_border', #public function
           ]
__version__ = '3.3.2'
__author__ = 'ShiraiTK'

from collections import Counter, defaultdict
from contextlib import contextmanager
from itertools import chain, product, zip_longest
from statistics import mean, median, variance, stdev #平均: mean, 中央値: median, 分散: variance, 標準偏差: stdev
import copy
import functools
import inspect
import io
import os
import re
import subprocess
import unicodedata

#ファイルを開くコマンド
if os.name == 'nt': #Windows
    _OPEN_CMD = ['cmd.exe', '/C', 'start']
else:
    _OPEN_CMD = None

#------------------------------
# デコレータ
#------------------------------
def set_row_range(func):
    """
    メソッドの引数row_start_idxとrow_end_idxの値をself.data_row_rangeで設定する
        func呼び出し時にrow_start_idxやrow_end_idxが指定されていれば、その指定を優先する
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        #funcの引数を全てall_kwargsにまとめる
        spec = inspect.getfullargspec(func)
        spec_args_len = len(spec.args)
        if spec.args[0] == 'self':
            spec.args.pop(0)
        all_kwargs = dict(zip(spec.args, args[:spec_args_len]))
        if spec.varargs is not None:
            all_kwargs[spec.varargs] = args[spec_args_len]
        if spec.kwonlydefaults is not None:
            all_kwargs.update(spec.kwonlydefaults)
        all_kwargs.update(kwargs)

        #row_start_idx, row_end_idxを設定
        #   func呼び出し時にrow_start_idxやrow_end_idxが指定されていれば、その指定を優先する
        key = 'row_start_idx'
        if key not in all_kwargs:
            all_kwargs[key] = self.data_row_range.start

        key = 'row_end_idx'
        if key not in all_kwargs:
            all_kwargs[key] = self.data_row_range.stop
        
        #print(f'all_kwargs: {all_kwargs}') ###
        return func(self, **all_kwargs)
    return wrapper

def add_print_contextmanager(func):
    """
    print関連のメソッドに前後処理(self.print_contextmanager)を追加する
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.print_contextmanager is None:
            def print_contextmanager(arg): yield
        else:
            print_contextmanager = self.print_contextmanager

        with contextmanager(print_contextmanager)(self):
            func(self, *args, **kwargs)
    return wrapper

#------------------------------
# PrintContextManagerクラス
#------------------------------
class PrintContextManager(object):
    @staticmethod
    def aggregate(func=None):
        """
        funcで集計した各行と各列の集計値をprin関連メソッド表示時に追加表示する
        """
        @functools.wraps(PrintContextManager.aggregate)
        def contextmanager_func(tda_self):
            column = tda_self.map_rows(func)
            if tda_self.header_idx is not None:
                column[tda_self.header_idx] = f'{func.__name__}' #ヘッダー位置に情報付加
            tda_self.add_column(None, column)
            tda_self.data.append(tda_self.map_columns(func))
            yield
            del(tda_self.data[-1])
            tda_self.del_column(-1)
            print(f'Add aggregate: {func.__name__}')
        return contextmanager_func

    @staticmethod
    def aggregate_row(func=None):
        """
        funcで集計した各行の集計値をprin関連メソッド表示時に追加表示する
        """
        @functools.wraps(PrintContextManager.aggregate_row)
        def contextmanager_func(tda_self):
            column = tda_self.map_rows(func)
            if tda_self.header_idx is not None:
                column[tda_self.header_idx] = f'{func.__name__}' #ヘッダー位置に情報付加
            tda_self.add_column(None, column)
            yield
            tda_self.del_column(-1)
            print(f'Add aggregate_row: {func.__name__}')
        return contextmanager_func

    @staticmethod
    def aggregate_col(func=None):
        """
        funcで集計した各列の集計値をprin関連メソッド表示時に追加表示する
        """
        @functools.wraps(PrintContextManager.aggregate_col)
        def contextmanager_func(tda_self):
            tda_self.data.append(tda_self.map_columns(func))
            yield
            del(tda_self.data[-1])
            print(f'Add aggregate_col: {func.__name__}')
        return contextmanager_func

    @staticmethod
    def aggregate_line(func=None, header_field=None):
        """
        header_fieldで指定した列を集計対象とし、
        funcで集計した各行と各列の集計値をprin関連メソッド表示時に追加表示する
        """
        @functools.wraps(PrintContextManager.aggregate_line)
        def contextmanager_func(tda_self):
            if not tda_self._exists_header():
                yield
                print(f"Can't add aggregate_line: {func.__name__}({header_field})")
            else:
                idx = tda_self[header_field]
                start = tda_self.data_row_range.start
                stop = tda_self.data_row_range.stop
                line = [tda_self.split_multiplelines(field) if isinstance(field, str) and tda_self.multiple_lines else [field]
                        for field in tda_self.get_column(idx)[start:stop]]

                #追加する列
                top = ['' for _ in range(len(tda_self.data[0:start]))]
                bottom = [] if stop is None else ['' for _ in range(len(tda_self.data[stop:]))]
                column = top + [func(field) for field in line] + bottom
                column[tda_self.header_idx] = f'{func.__name__}({header_field})' #ヘッダー位置に情報付加
                tda_self.add_column(None, column)

                #追加する行
                row = ['' for _ in range(tda_self.shape()[1])]
                agg = func(list(chain.from_iterable(line)))
                row[idx] = agg
                row[-1] = agg
                tda_self.data.append(row)
                yield
                del(tda_self.data[-1])
                tda_self.del_column(-1)
                print(f'Add aggregate_line: {func.__name__}({header_field})')
        return contextmanager_func

#------------------------------
# Wrapperクラス
#------------------------------
class Wrapper(object):
    @staticmethod
    def non_error(func, err_value=''):
        """
        func関数のエラーを吸収するラッパー関数
            err_value: エラーの場合に返す値
        """
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                ret = func(*args, **kwargs)
            except:
                ret = err_value
            return ret
        return wrapper_func

    @staticmethod
    def arg_of_numlist(func):
        """
        引数を加工するラッパー関数
        iterableの要素から数字要素のみを取り出したリストを引数にする
        """
        @functools.wraps(func)
        def wrapper_func(iterable):
            if hasattr(iterable, '__iter__'):
                num_lst = [i for i in iterable if isinstance(i, int) or isinstance(i, float)] #数字以外は除外
            else:
                raise TypeError(f'unsupported {type(iterable)}')
            return func(num_lst)
        return wrapper_func

    @staticmethod
    def arg_of_strlist(func):
        """
        引数を加工するラッパー関数
        iterableの要素から文字列要素のみを取り出したリストを引数にする
        """
        @functools.wraps(func)
        def wrapper_func(iterable):
            if hasattr(iterable, '__iter__'):
                num_lst = [i for i in iterable if isinstance(i, str)] #文字列以外は除外
            else:
                raise TypeError(f'unsupported {type(iterable)}')
            return func(num_lst)
        return wrapper_func

    @staticmethod
    def support_multiplelines(func, multiple_lines_delimiter):
        """
        multiple-linesを処理するラッパー関数
        引数にmultiple-linesのフィールドが含まれていればそれを展開したリストを引数にする
        funcで処理した結果を再びmultiple-linesに変換して返す
            f = support_multiplelines(lambda x: x*2, '\\n')
            f('1\\n2\\n3') -> '2\\n4\\n6'
        """
        @functools.wraps(func)
        def wrapper_func(*args):
            #multiple-linesがあるかチェック
            if all([isinstance(i, str) and multiple_lines_delimiter in i for i in args]):
                new_args = zip(*[[_str2int_or_float(line) for line in arg.split(multiple_lines_delimiter)] for arg in args])
                return multiple_lines_delimiter.join([str(func(*new_arg)) for new_arg in new_args])
            else:
                return func(*args)

        return wrapper_func

    @staticmethod
    def _arg_of_flatten_multiplelines_list(func, multiple_lines_delimiter):
        """
        引数を加工するラッパー関数
        multiple-linesのフィールドが含まれていればそれを展開したリストを引数にする
            ['hoge\\nfuga\\n123', 4, 5] -> ['hoge', 'fuga', 123, 4, 5]
        """
        @functools.wraps(func)
        def wrapper_func(iterable):
            if hasattr(iterable, '__iter__'):
                pass
            else:
                raise TypeError(f'unsupported {type(iterable)}')

            #multiple-linesがあるかチェック
            if any([multiple_lines_delimiter in i for i in [i for i in iterable if isinstance(i, str)]]):
                new_lst = []
                [new_lst.extend(i.split(multiple_lines_delimiter))
                    if isinstance(i,str) and multiple_lines_delimiter in i
                    else new_lst.append(i) for i in iterable]
                new_lst = [_str2int_or_float(i) for i in new_lst]
                return func(new_lst)
            else:
                return func(iterable)
        return wrapper_func

#------------------------------
# Magicクラス
#------------------------------
class Magic(object):
    @staticmethod
    def is_magic(tda_data, info={}, verbose=True):
        """
        tda_dataが魔方陣か判定する
            info: 辞書を設定して呼び出せば通常より詳しい判定情報(magic_info)を渡す
            verbose: Trueならば通常より詳しい判定情報(magic_info)を表示する
        """
        magic_info = {'natural_num':False, 'row_sum':None, 'col_sum':None, 'slash_sum':None, 'bslash_sum':None}

        #tda_dataが1から始まる連番かどうかをチェック
        #数字以外のフィールド値は無視
        tda_data_elements = sorted(i for i in set(chain.from_iterable(tda_data))
                                   if isinstance(i,int) or isinstance(i,float))
        if tda_data_elements == list(range(1, tda_data_elements[-1]+1)):
            magic_info['natural_num'] = True

        #各行の合計値
        sum_nums = Wrapper.arg_of_numlist(sum)
        row_sum = tuple(sum_nums(row) for row in tda_data)
        set_row_sum = set(row_sum)
        if len(set_row_sum) == 1:
            row_sum = list(set_row_sum)[0] #全部同じ値なら1つにまとめる
        magic_info['row_sum'] = row_sum

        #各列の合計値
        col_sum = tuple(sum_nums(col) for col in row2column(tda_data))
        set_col_sum = set(col_sum)
        if len(set_col_sum) == 1:
            col_sum = list(set_col_sum)[0] #全部同じ値なら1つにまとめる
        magic_info['col_sum'] = col_sum

        #対角線の合計値
        tda_data_low_len = len(tda_data[0])
        magic_info['slash_sum'] = sum_nums([tda_data[i][-i-1] for i in range(tda_data_low_len)])
        magic_info['bslash_sum'] = sum_nums([tda_data[i][i] for i in range(tda_data_low_len)])

        if isinstance(info, dict):
            info.update(magic_info) #info引数に辞書を設定して本関数を呼び出せばmagic_infoを渡す

        if verbose:
            [print(f'{key:12s}: {value}') for key, value in magic_info.items()]

        if magic_info['natural_num'] and len(set(magic_info[key] for key in magic_info if key != 'natural_num'))==1:
            return True
        else:
            return False

    @staticmethod
    def magic(magic_num=3):
        """
        魔方陣を作成する
        """
        if magic_num >= 3:
            pass
        else:
            return #3以下の数字は無視

        if magic_num % 2 == 0:
            return Magic._even_magic(magic_num)
        else:
            return Magic._odd_magic(magic_num)

    @staticmethod
    def _odd_magic(odd_number=3):
        """
        奇数辺の魔方陣を作成する
        """
        m = list2tda(list(range(1, odd_number**2+1)), odd_number)
        m.rotate_r45()

        center_idx = m._row_center()
        extra = (m._row_len() - odd_number) // 2
        def marge(lst1, lst2):
            [lst1.pop(idx) or lst1.insert(idx, lst2_data) if lst1_data=='' and lst2_data!='' else None
             for idx,(lst1_data,lst2_data) in enumerate(zip(lst1, lst2))]

        def puzzle():
            piece_top = m.data[:extra]
            piece_btm = m.data[-extra:]
            m.data = m.data[extra:-extra]
            area_top = m.data[:extra]
            area_btm = m.data[-extra:]
            [marge(lst1, lst2) for area, piece in [(area_btm, piece_top), (area_top, piece_btm)] for lst1, lst2 in zip(area, piece)]

        puzzle()
        m.rotate_r90()
        puzzle()
        m.rotate_l90()

        return m

    @staticmethod
    def _flat(tda_data):
        """
        tda_dataの縦横の合計値の差異が少なくなるように整える
        """
        m = TwoDimArray(tda_data)
        m.row2column()
        m.data = [row if row_idx%2==0 else [i for i in row[::-1]] for row_idx, row in enumerate(m.data)]
        #m.print2() ###
        #Magic.is_magic(m.data) ###
        return m

    @staticmethod
    def _even_magic(even_number=4):
        """
        偶数辺の魔方陣を作成する
        """
        m = list2tda(list(range(1, even_number**2+1)), even_number)

        #TwoDimArrayをフラット化
        magic_info = {'slash_sum':True, 'bslash_sum':False} #値はダミー
        while magic_info['slash_sum'] != magic_info['bslash_sum']:
            m = Magic._flat(m.data)
            Magic.is_magic(m.data, magic_info, verbose=False)

        #対角線を含まない各斜め要素を直行する対角軸で反転
        slash = m.get_slash() #対角線(スラッシュ)
        slash_stripe = m.get_slash_stripe() - slash #対角線要素を削除
        slash_stripe.invert_bslash()

        bslash = m.get_bslash() #対角線(バックスラッシュ)
        bslash_stripe = m.get_bslash_stripe() - bslash #対角線要素を削除
        bslash_stripe.invert_slash()

        m = m.get_diagonal() + slash_stripe + bslash_stripe
        if Magic.is_magic(m.data, magic_info, verbose=False): #魔方陣になっていれば完了
            return m
        #m.print2(); (m-m.get_diagonal()).print2(); Magic.is_magic(m.data) ###

        #各行列の合計値を揃える
        #   8x8
        #   +--+--+--+--+--+--+--+--+   +--+--+--+--+--+--+--+--+
        #   | 1|63|62|61|60|59|58| 8|   | 0|63|62|61|60|59|58| 0|
        #   +--+--+--+--+--+--+--+--+   +--+--+--+--+--+--+--+--+
        #   |56|10|54|53|52|51|15|49|   |56| 0|54|53|52|51| 0|49| <-対角線の外側から入れ替えていく(56<->16, 49<->9)
        #   +--+--+--+--+--+--+--+--+   +--+--+--+--+--+--+--+--+   対角線の外側を全部入れ替えてもまだ入れ替える必要があれば
        #   |48|47|19|45|44|22|42|41|   |48|47| 0|45|44| 0|42|41|   次は中心から入れ替える(53<->13)
        #   +--+--+--+--+--+--+--+--+   +--+--+--+--+--+--+--+--+   これでインデックス1,-1の行の合計値が揃った
        #   |40|39|38|28|29|35|34|33|   |40|39|38| 0  0|35|34|33|
        #   +--+--+--+--+--+--+--+--+   +--+--+--+  +  +--+--+--+
        #   |32|31|30|36|37|27|26|25|   |32|31|30| 0  0|27|26|25|
        #   +--+--+--+--+--+--+--+--+   +--+--+--+--+--+--+--+--+
        #   |24|23|43|21|20|46|18|17|   |24|23| 0|21|20| 0|18|17|
        #   +--+--+--+--+--+--+--+--+   +--+--+--+--+--+--+--+--+
        #   |16|50|14|13|12|11|55| 9|   |16| 0|14|13|12|11| 0| 9| <-
        #   +--+--+--+--+--+--+--+--+   +--+--+--+--+--+--+--+--+
        #   |57| 7| 6| 5| 4| 3| 2|64|   | 0| 7| 6| 5| 4| 3| 2| 0|
        #   +--+--+--+--+--+--+--+--+   +--+--+--+--+--+--+--+--+
        center = m._row_center()
        length = m._row_len()
        indexs = list(range(length))
        total_value = magic_info['slash_sum']
        def align_total_value(sum_info):
            for row_idx, row_sum in enumerate(sum_info[:center]):
                difference = abs(total_value - row_sum)
                #print(f'row_idx: {row_idx}, row_sum: {row_sum}, difference: {difference}, m.data[row_idx]: {m.data[row_idx]}')###
                l = list(chain.from_iterable(zip(indexs[:center][:row_idx][::-1] + indexs[:center][row_idx:][::-1],
                                                 indexs[center:][-row_idx:] + indexs[center:][:-row_idx])))
                num = difference // abs(m.data[row_idx][l[0]] - m.data[-row_idx-1][l[0]]) #入れ替える数
                for col_idx in l[:num]:
                    m.data[row_idx][col_idx], m.data[-row_idx-1][col_idx] = m.data[-row_idx-1][col_idx], m.data[row_idx][col_idx]

        #各行の合計値を揃える
        align_total_value(magic_info['row_sum'])

        #各列の合計値を揃える
        m.row2column()
        align_total_value(magic_info['col_sum'])
        m.row2column()

        #Magic.is_magic(m.data)
        return m

#------------------------------
# TwoDimArrayクラス
#------------------------------
class TwoDimArray(object):
    _DEFAULT_NAME = ''
    _DEFAULT_HEADER_IDX = None
    _DEFAULT_DATA_ROW_RANGE = slice(0, None)
    _DEFAULT_PRINT2_BORDER = 'Standard'
    _DEFAULT_PRINT_IDX2_BORDER = 'Index'
    _DEFAULT_BORDER_GROUPING = True

    _DEFAULT_MULTIPLE_LINES = True
    _DEFAULT_MULTIPLE_LINES_DELIMITER = r'\n'

    _DEFAULT_GROUPING_OPT = True
    _DEFAULT_PRECISION = 2
    _DEFAULT_DISPLAY_DELIMITER = ', '
    _DEFAULT_HEAD = 5
    _DEFAULT_PRINT_FILE = {'file':None, 'encoding':None}
    _DEFAULT_PRINT_CONTEXTMANAGER = None

    def __init__(self, tda_data=None):
        """
        tda_dataはリストの2次元配列( tda_dataの最小構成は[['']] )
        """
        if tda_data is None:
            tda_data = [['']]

        #tda_dataがリストの2次元配列かチェック
        if (isinstance(tda_data, list) and bool(tda_data) #tda_dataはリストで何か入っている
            and isinstance(tda_data[0], list) and bool(tda_data[0])): #入ってるのはリストで、さらに何か(データ)入っていればOK
            self.data = tda_data
        else:
            raise ValueError(f"TwoDimArray()の引数tda_dataはリストの2次元配列を期待しています(tda_dataの最小構成は[['']]): {repr(tda_data)}")

        self.reset_property() #プロパティの初期設定

    def reset_property(self):
        """
        プロパティをデフォルト値に戻す
        """
        self.name = TwoDimArray._DEFAULT_NAME #TwoDimArrayの名前
        self.header_idx = TwoDimArray._DEFAULT_HEADER_IDX #ヘッダーのインデックス
        self.data_row_range = TwoDimArray._DEFAULT_DATA_ROW_RANGE #TwoDimArrayでヘッダー＆フッターを含まないデータ範囲(sliceで設定)
        self.print2_border = TwoDimArray._DEFAULT_PRINT2_BORDER #print2メソッドで使用するborder_pattern
        self.print_idx2_border = TwoDimArray._DEFAULT_PRINT_IDX2_BORDER #print_idx2メソッドで使用するborder_pattern
        self.border_grouping = TwoDimArray._DEFAULT_BORDER_GROUPING #Trueにすると枠のグループ化機能が有効になる

        self.multiple_lines = TwoDimArray._DEFAULT_MULTIPLE_LINES #Trueにするとフィールド値をmultiple_lines_delimiterで枠内改行して表示する
        self.multiple_lines_delimiter = TwoDimArray._DEFAULT_MULTIPLE_LINES_DELIMITER #フィールド値をmultiple-linesに変換するデリミタ

        self.grouping_opt = TwoDimArray._DEFAULT_GROUPING_OPT #Trueにすると数字の可読性があがる(千倍ごとの数字の区切り文字にアンダースコアを使う: 12345 -> 12_345)
        self.precision = TwoDimArray._DEFAULT_PRECISION #floatの精度(小数点以下の桁数)
        self._display_delimiter = TwoDimArray._DEFAULT_DISPLAY_DELIMITER #表示用デリミタ
        self._head = TwoDimArray._DEFAULT_HEAD #print関数で表示するself.dataの先頭からの行数
        self.print_file = TwoDimArray._DEFAULT_PRINT_FILE.copy() #設定したファイルにprint関連メソッドの出力が上書き保存される
        self.print_contextmanager = TwoDimArray._DEFAULT_PRINT_CONTEXTMANAGER #print関連メソッドの前後処理を行うcontextmanagerを登録できる(contextmanagerにはselfが渡される)

    def _copy_property(self, src):
        """
        src.data以外のプロパティをsrcからコピーする
            filterメソッドやmap_fieldメソッドなど、処理結果を新しいTwoDimArrayインスタンスとして返すメソッドで使用する
        """
        self.name = src.name
        self.header_idx = src.header_idx
        self.data_row_range = src.data_row_range
        self.print2_border = src.print2_border
        self.print_idx2_border = src.print_idx2_border
        self.border_grouping = src.border_grouping

        self.multiple_lines = src.multiple_lines
        self.multiple_lines_delimiter = src.multiple_lines_delimiter

        self.grouping_opt = src.grouping_opt
        self.precision = src.precision
        self._display_delimiter = src._display_delimiter
        self._head = src._head
        self.print_file = src.print_file.copy()
        self.print_contextmanager = src.print_contextmanager

    def __call__(self, *args):
        """
        get_field_idxメソッドの簡易版
        """
        return self.get_field_idx(*args)

    def __getitem__(self, header_value):
        """
        get_header_idxメソッドの簡易版
        """
        if isinstance(header_value, tuple):
            return self.get_header_idx(*header_value)
        else:
            return self.get_header_idx(header_value)

    def _row_len(self):
        return len(self.data)

    def _col_len(self):
        return len(self.data[0])

    def _row_center(self):
        return self._row_len()//2

    def _col_center(self):
        return self._col_len()//2

    #------------------------------
    # 演算子
    #------------------------------
    def __add__(self, other):
        return TwoDimArray._cal_tda(self, other, lambda x,y: x+y)

    def __sub__(self, other):
        return TwoDimArray._cal_tda(self, other, lambda x,y: x-y)

    @staticmethod
    def _cal_tda(tda1, tda2, operator):
        if all(isinstance(i, TwoDimArray) for i in (tda1, tda2)):
            tda_data = [[TwoDimArray._cal_field(self_field, other_field, operator)
                        for self_field, other_field in zip_longest(self_row, other_row, fillvalue='')]
                        for self_row, other_row in zip_longest(tda1.data, tda2.data, fillvalue='')]
            new_tda = TwoDimArray(tda_data)
            new_tda._copy_property(tda1)
            return new_tda

    @staticmethod
    def _cal_field(field1, field2, operator):
        blank = '' #空フィールド
        fields = [field for field in (field1, field2) if field != blank]
        if len(fields) == 0:
            return blank #どちらも空フィールドなら空フィールドを返す
        elif len(fields) == 1:
            return fields[0] #どちらかが空フィールドなら空フィールドじゃない方を返す
        else:
            try:
                new_field = operator(*fields)
            except TypeError:
                #エラー箇所が分かりやすいようにエラー情報追加
                print(f'ERROR: {operator}({repr(fields[0])}, {repr(fields[1])})')
                raise

            return new_field

    #------------------------------
    # 表示
    #------------------------------
    def __str__(self):
        return self._sprint(head=self._head)

    def _sprint(self, head=None, tail=None, header_aligns=None, aligns=None, widths=None, _chk_multiple_lines=True):
        """
        self.dataの行列文字列を返す
            head: 先頭からの行数を指定
            tail: 最後尾からの行数を指定

            _chk_multiple_lines: multiple-lines処理をするか否かのスイッチ
                                 print2, print_idx2メソッドなどの枠付きでは枠の処理でmultiple-lines処理をするため不要となる
        """
        if tail is not None:
            head = None #tail優先
            tail = -tail #-tailで最後尾からのインデックスに変換

        return self._sprint_range(row_start_idx=tail, row_end_idx=head, 
                                  header_aligns=header_aligns, aligns=aligns, widths=widths, _chk_multiple_lines=_chk_multiple_lines)

    def _sprint_range(self, row_start_idx=0, row_end_idx=None, header_aligns=None, aligns=None, widths=None, _chk_multiple_lines=True):
        """
        指定された行範囲の文字列を返す
            ※TwoDimArray文字列化の共通関数
        """
        if self.multiple_lines and _chk_multiple_lines:
            m_tda, _ = self._extend_multiple_lines()
            tda = self if m_tda is None else m_tda
        else:
            tda = self

        return tda._tda_string_format(row_start_idx=row_start_idx, row_end_idx=row_end_idx, header_aligns=header_aligns, aligns=aligns, widths=widths)

    @add_print_contextmanager
    def print(self, head=None, tail=None):
        """
        self.dataを行列表示する
        """
        with self._print_strings() as strings:
            strings.append(self._sprint(head=head, tail=tail))

    @add_print_contextmanager
    def print2(self, head=None, tail=None):
        """
        self.dataの行列を枠で囲んで見やすくして表示する
        """
        wrap_tda = self.wrap_border(self.print2_border)
        with self._print_strings() as strings:
            #multiple-linesの処理はwrap_borderメソッドで処理済み
            strings.append(wrap_tda._sprint(head=head, tail=tail, _chk_multiple_lines=False))

    @add_print_contextmanager
    def print_idx(self, head=None, tail=None):
        """
        self.dataに行と列のインデックス情報を付け加えて行列表示する
        """
        idx_tda = self._add_idx()
        with self._print_strings() as strings:
            strings.append(idx_tda._sprint(head=head, tail=tail, aligns={0:'>'})) #文字列のインデックスを右寄りに配置

    @add_print_contextmanager
    def print_idx2(self, head=None, tail=None):
        """
        self.dataに行と列のインデックス情報を付け加え、さらに枠で囲んで見やすくした行列を表示する
        """
        idx_tda = self._add_idx()
        wrap_tda = idx_tda.wrap_border(idx_tda.print_idx2_border, aligns={0:'>'}) #文字列のインデックスを右寄りに配置
        with self._print_strings() as strings:
            #multiple-linesの処理はwrap_borderメソッドで処理済み
            strings.append(wrap_tda._sprint(head=head, tail=tail, _chk_multiple_lines=False))

    @add_print_contextmanager
    def print_chg_format(self, head=None, tail=None, header_aligns=None, aligns=None, widths=None):
        """
        列のalignやwidthをカスタマイズして表示する
        """
        with self._print_strings() as strings:
            strings.append(self._sprint(head=head, tail=tail,
                                        header_aligns=header_aligns, aligns=aligns, widths=widths))

    @add_print_contextmanager
    def print_range(self, row_start_idx=0, row_end_idx=None):
        """
        self.dataを行列表示する
            指定した行のインデックス範囲を表示する
        """
        with self._print_strings() as strings:
            strings.append(self._sprint_range(row_start_idx=row_start_idx, row_end_idx=row_end_idx))

    def _add_idx(self):
        """
        行と列のインデックス表示のために、インデックス情報を加えたTwoDimArrayインスタンスを返す
        (print_idxとprint_idx2の共通処理)
        """
        columns = row2column(self.data)
        columns.insert(0, [str(i) for i in range(len(columns[0]))]) #左端の列に文字列のインデックス追加
        columns.append([str(i) for i in range(len(columns[0]))]) #右端の列に文字列のインデックス追加
        rows = row2column(columns)

        max_col_num = max([len(row) for row in rows])
        index = ['index'] + [str(i) for i in range(max_col_num-2)] + ['index'] #max_col_num-2: 前後の'index'分減らす
        rows.insert(0, index) #先頭の行に文字列のインデックス追加
        rows.append(index) #最後尾の行に文字列のインデックス追加

        idx_tda = TwoDimArray(rows)
        idx_tda._copy_property(self)
        return idx_tda

    def _extend_multiple_lines(self, border_tda=None):
        """
        self.dataの一行表現のmultiple-linesを複数行表現に展開したTwoDimArrayインスタンスを返す(multiple-linesが無ければNoneを返す)
            ・border_tda: self.dataを収められる枠パターンのTwoDimArrayインスタンス
                          指定すると複数行に展開されたTwoDimArrayが収まる枠パターンのTwoDimArrayインスタンスも返す
                          (multiple-linesが無い、もしくは未指定ならばNoneを返す)
                            
                            new_tda, _ = self._extend_multiple_lines()
                            new_tda, new_p_tda = self._extend_multiple_lines(p_tda)
        """
        multiple_lines_idxs = self.get_string_idx_all(self.multiple_lines_delimiter)
        if not multiple_lines_idxs:
            return (None, None)
        #print(f'multiple_lines_idxs: {multiple_lines_idxs}') ###

        tda_data = copy.deepcopy(self.data)
        def field2multiple_lines(row_idx, col_idx): #一行表現のmultiple-linesを複数行表現(リスト)に変換
            tda_data[row_idx][col_idx] = [_str2int_or_float(field) for field in tda_data[row_idx][col_idx].split(self.multiple_lines_delimiter)]
        [field2multiple_lines(row_idx, col_idx) for row_idx, col_idx in multiple_lines_idxs]
        #print(f'tda_data: {tda_data}') ###

        increase_row = {}
        multiple_lines_row_idxs = sorted(set(row_idx for row_idx, col_idx in multiple_lines_idxs))
        def multiple_lines2zip_longest(row_idx): #multiple-linesのある行をmultiple-linesの行数に拡張
            tda_data[row_idx] = [list(i) for i in #zip_longestでタプルになった要素をリストに戻す
                                 zip_longest(*[[field] if not isinstance(field, list) else field for field in tda_data[row_idx]],
                                             fillvalue='')]
            increase_row[row_idx] = len(tda_data[row_idx])-1
        [multiple_lines2zip_longest(row_idx) for row_idx in multiple_lines_row_idxs]
        #print(f'tda_data: {tda_data}') ###
        #print(f'increase_row: {increase_row}') ###
        #print(f'multiple_lines_row_idxs: {multiple_lines_row_idxs}') ###

        new_tda_data = []
        [new_tda_data.extend(row_value) if row_idx in multiple_lines_row_idxs else new_tda_data.append(row_value)
         for row_idx, row_value in enumerate(tda_data)]
        #print(f'new_tda_data: {new_tda_data}') ###
        new_tda = TwoDimArray(new_tda_data)
        new_tda._copy_property(self)

        if border_tda is not None:
            #border_tda.print() ###
            border_increase_row = dict([(row_idx*2+1, increase) for row_idx, increase in increase_row.items()])
            border_data = copy.deepcopy(border_tda.data)
            def row_increase(row_idx):
                spaces = tuple(' ' for _ in range(len(border_data[row_idx])))
                border = tuple(border_data[row_idx])
                border_data[row_idx] = [list(i) for i in [border] + [spaces, border] * border_increase_row[row_idx]]
                #print(f'border_data: {border_data[row_idx]}') ###
            [row_increase(row_idx) for row_idx in border_increase_row.keys()]

            new_border_data = []
            [new_border_data.extend(row_value) if row_idx in border_increase_row.keys() else new_border_data.append(row_value)
             for row_idx, row_value in enumerate(border_data)]
            #print(f'border_data: {border_data}') ###
            #b=TwoDimArray(border_data);b._display_delimiter='';b.print() ###
            new_border_tda = TwoDimArray(new_border_data)
            new_border_tda._copy_property(border_tda)
            #new_border_tda.print() ###
            return (new_tda, new_border_tda)

        return (new_tda, None)

    @contextmanager
    def _print_strings(self):
        """
        print関連のメソッドの共通処理
        """
        strings = []
        yield strings

        strings = ' '.join(strings)
        if self.print_file['file'] is not None:
            self._write_print_file(strings)
        else:
            print(strings)

    def shape(self):
        """
        TwoDimArrayの行と列の長さを返す
        """
        self.fill() #TwoDimArrayに欠損があれば埋める
        return (self._row_len(), self._col_len())

    def counter_row(self, row_idx):
        """
        指定行(row_idx)のCounterを返す
        """
        return Counter(self.data[row_idx])

    def counter_column(self, col_idx):
        """
        指定列(col_idx)のCounterを返す
        """
        return Counter([self.data[row_idx][col_idx] for row_idx in range(len(self.data))])

    def _fields_string_format(self, row_start_idx=0, row_end_idx=None, header_aligns=None, aligns=None, widths=None):
        """
        self.dataの行列の各フィールドを文字列にして返す
            各列の文字列幅を均一にする(全角文字が混じっていてもズレません)
            self.dataの行範囲[row_start_idx:row_end_idx]を指定可能

            各列の書式指定を個別に指定できる:
                ・header_aligns: ヘッダーのalignを設定する辞書{列インデックス: align} (align: 左詰め='<'、右詰め='>', 中央寄せ='^')
                ・aligns: 各列のalignを設定する辞書{列インデックス: align} (align: 左詰め='<'、右詰め='>', 中央寄せ='^')
                ・widths: 各列のwidthを設定する辞書{列インデックス: width}
            ※列インデックスで指定されていない他の全ての設定をNoneキーで設定できる
        """
        tda_data = self.data[row_start_idx:row_end_idx]
        columns = row2column(tda_data)

        #align設定
        col_aligns = ['' for _ in columns] #''はalign無し(デフォルトのalign設定が適用される)
        if aligns is not None and isinstance(aligns, dict):
            other_align = aligns.get(None)
            if other_align:
                col_aligns = [other_align for _ in columns]

            col_aligns = [aligns.get(col_idx) if aligns.get(col_idx) is not None else col_align 
                          for col_idx, col_align in enumerate(col_aligns)]
            #print(f'col_aligns: {col_aligns}(カスタム化)') ###

        #width設定
        col_max_widths = _max_widths(columns, grouping_opt=self.grouping_opt, precision=self.precision) #各列の最大文字列幅
        #print(f'col_max_widths: {col_max_widths}') ###
        #print(f'widths: {widths}') ###
        if widths is not None and isinstance(widths, dict):
            other_width = widths.get(None)
            if other_width:
                c_widths = defaultdict(lambda:other_width)
            else:
                c_widths = defaultdict(lambda:0)
            c_widths.update(widths)
            col_max_widths = [c_widths[col_idx] if c_widths[col_idx] > col_max_width else col_max_width 
                              for col_idx, col_max_width in enumerate(col_max_widths)]
            #print(f'col_max_widths: {col_max_widths}(カスタム化)') ###

        #ヘッダーalign設定
        h_aligns = col_aligns[:] #初期設定はcol_aligns
        if header_aligns is not None and isinstance(header_aligns, dict):
            other_header_align = header_aligns.get(None)
            if other_header_align:
                h_aligns = [other_header_align for _ in h_aligns]

            h_aligns = [header_aligns.get(col_idx) if header_aligns.get(col_idx) is not None else h_align
                        for col_idx, h_align in enumerate(h_aligns)]
        #print(f'h_aligns: {h_aligns}') ###

        def get_format(row_idx, col_idx, field):
            #align
            if row_idx == self.header_idx: #ヘッダー
                align = h_aligns[col_idx]
            else:
                align = col_aligns[col_idx]

            #width
            width = col_max_widths[col_idx] - _count_em(str(field))
            if width <= 0:
                #fieldが空だとwidthがゼロになるが、
                #書式指定文字列の指定でalignが空('')で、かつ、widthがゼロだとValueErrorとなる
                #そのためwidthがゼロの場合は空('')を返す
                width = ''

            #数字の区切り文字
            grouping_option = ''
            if self.grouping_opt:
                if isinstance(field, str):
                    pass
                elif isinstance(field, int) or isinstance(field, float):
                    grouping_option = '_' #アンダースコア以外にカンマも設定可能だがcsvの区切り文字と同じなのでカンマは使用しない

            #精度
            dot_precision_type = ''
            if isinstance(field, float):
                dot_precision_type = f'.{self.precision}f'

            return f'{align}{width}{grouping_option}{dot_precision_type}'

        def get_data(field):
            if isinstance(field, str) or isinstance(field, int) or isinstance(field, float):
                return field
            else:
                return str(field)

        return [[f'{get_data(col_data):{get_format(row_idx, col_idx, col_data)}}' for col_idx, col_data in enumerate(row_data)]
                for row_idx, row_data in enumerate(tda_data)]

    def _tda_string_format(self, row_start_idx=0, row_end_idx=None, header_aligns=None, aligns=None, widths=None):
        """
        self.dataの行列を文字列にして返す
            各列の文字列幅を均一にする(全角文字が混じっていてもズレません)
            self.dataの行範囲[row_start_idx:row_end_idx]を指定可能

            各列の書式指定を個別に指定できる:
                ・header_aligns: ヘッダーのalignを設定する辞書{列インデックス: align} (align: 左詰め='<'、右詰め='>', 中央寄せ='^')
                ・aligns: 各列のalignを設定する辞書{列インデックス: align} (align: 左詰め='<'、右詰め='>', 中央寄せ='^')
                ・widths: 各列のwidthを設定する辞書{列インデックス: width}
            ※列インデックスで指定されていない他の全ての設定をNoneキーで設定できる
        """
        if row_start_idx is not None:
            remain_toplines_num = len(self.data[:row_start_idx])
        else:
            remain_toplines_num = 0

        if row_end_idx is not None:
            remain_bottomlines_num = len(self.data[row_end_idx:])
        else:
            remain_bottomlines_num = 0

        fields_str = self._fields_string_format(row_start_idx=row_start_idx, row_end_idx=row_end_idx, header_aligns=header_aligns, aligns=aligns, widths=widths)
        tda_str = '\n'.join([self._display_delimiter.join(row_data) for row_data in fields_str])

        if remain_toplines_num:
            tda_str = f'↑(There are {remain_toplines_num} rows)\n' + tda_str
        if remain_bottomlines_num:
            tda_str += f'\n↓(There are {remain_bottomlines_num} rows)'

        return tda_str

    #------------------------------
    # 保存
    #------------------------------
    def save(self, csv_file, mode='w', encoding=None, uniform=True):
        """
        csvファイル(csv_file)にTwoDimArray(self.data)を保存する
            uniform=True: 各列の文字幅を均一にする
        """
        with open(csv_file, mode, encoding=encoding) as f:
            if uniform:
                f.write(self._sprint()+'\n')
            else:
                f.write('\n'.join([','.join(row) for row in _field2striped_str(self.data)])+'\n')

    def set_print_file(self, f_name=None, encoding=None):
        """
        print関連のメソッドの出力先をファイル(f_name)に変更する
            Windowsの場合はOSに関連付けられたアプリケーションでファイルを開く処理も行う
        """
        if f_name is None and encoding is None:
            self.print_file = TwoDimArray._DEFAULT_PRINT_FILE.copy() #初期化
            return

        if os.path.exists(f_name):
            mode = 'r'
        else:
            mode = 'w' #f_nameファイルが無ければ作成

        try:
            with open(f_name, mode=mode, encoding=encoding) as f:
                pass
        except:
            raise

        self.print_file.update({'file': f_name, 'encoding': encoding})
        if _OPEN_CMD:
            subprocess.run(_OPEN_CMD + [f_name]) #OSに関連付けられたアプリケーションでファイルを開く

    def _write_print_file(self, strings):
        """
        print関連のメソッドの出力をファイル(self.print_file['file'])に書き込む
        """
        f_name = self.print_file['file']
        encoding = self.print_file['encoding']

        with open(f_name, mode='w', encoding=encoding) as f:
            root, ext = os.path.splitext(f_name)
            if ext == '.html':
                f.write(f'<PRE>\n{strings}\n</PRE>') #ブラウザで表示できるように<PRE>タグ(整形済みテキスト)で囲む
            else:
                f.write(strings)

    #------------------------------
    # ヘッダー確認
    #------------------------------
    def get_header(self):
        """
        TwoDimArrayのヘッダーを返す
        """
        if self._exists_header():
            return self.data[self.header_idx]

    def get_header_idx(self, value, start=None, stop=None):
        """
        TwoDimArrayのヘッダーの中にvalueがあればそのインデックスを返す
            self.get_header().index(value, start, stop)の結果を返す
        """
        if self._exists_header():
            args = [arg for arg in [value, start, stop] if arg is not None]
            idx = self.get_header().index(*args)
            return idx

    def get_header_value(self, idx):
        """
        TwoDimArrayのヘッダーにインデックスでアクセスしてその値を返す
            self.get_header()[idx]の結果を返す
        """
        if self._exists_header():
            header = self.get_header()[idx]
            return header

    def _exists_header(self):
        if self.header_idx is None:
            print('header_idx property is None')
            return False
        else:
            return True

    #------------------------------
    # フィールド確認
    #------------------------------
    def get_field_idx(self, value, row_idx=None, col_idx=None):
        """
        TwoDimArrayの中にvalueがあればそのインデックスを返す(最初に見つけた1つを返す)
            row_idx, col_idxで検索範囲を指定できる
            row_idx, col_idxはsliceも指定可能
        """
        for idxs in self._get_field_idx(value, row_idx, col_idx):
            return idxs

    def get_field_idx_all(self, value, row_idx=None, col_idx=None):
        """
        TwoDimArrayの中にvalueがあればそのインデックスを返す(見つけた全てを返す)
            row_idx, col_idxで検索範囲を指定できる
            row_idx, col_idxはsliceも指定可能
        """
        return [idxs for idxs in self._get_field_idx(value, row_idx, col_idx)]

    def get_string_idx(self, string, row_idx=None, col_idx=None):
        """
        TwoDimArrayの中にstringを含んだフィールドがあればそのインデックスを返す(最初に見つけた1つを返す)
            row_idx, col_idxで検索範囲を指定できる
            row_idx, col_idxはsliceも指定可能
        """
        for idxs in self._get_field_idx(string, partial_match=True, row_idx=row_idx, col_idx=col_idx):
            return idxs

    def get_string_idx_all(self, string, row_idx=None, col_idx=None):
        """
        TwoDimArrayの中にstringを含んだフィールドがあればそのインデックスを返す(見つけた全てを返す)
            row_idx, col_idxで検索範囲を指定できる
            row_idx, col_idxはsliceも指定可能
        """
        return [idxs for idxs in self._get_field_idx(string, partial_match=True, row_idx=row_idx, col_idx=col_idx)]

    def _get_field_idx(self, value, partial_match=False, row_idx=None, col_idx=None):
        """
        TwoDimArrayの中にvalueがあればそのインデックスを返す(get_field_idxとget_field_idx_allの共通処理)
            partial_match: Trueなら部分一致で判定(この場合はvalueは文字列であり、文字列のフィールドのみが対象となる)
                           Falseならば完全一致
            row_idx, col_idxで検索範囲を指定できる
            row_idx, col_idxはsliceも指定可能
        """
        if row_idx is None:
            rows = enumerate(self.data)
        elif isinstance(row_idx, slice):
            rows = enumerate(self.data[row_idx], start=row_idx.start)
        else:
            rows = enumerate(self.data[row_idx:row_idx+1], start=row_idx)

        if col_idx is None:
            cols = lambda row: enumerate(row)
        elif isinstance(col_idx, slice):
            cols = lambda row: enumerate(row[col_idx], start=col_idx.start)
        else:
            cols = lambda row: enumerate(row[col_idx:col_idx+1], start=col_idx)

        for r_idx, row in rows:
            for c_idx, field in cols(row):
                if partial_match: #部分一致
                    if isinstance(value, str) and isinstance(field, str) and value in field:
                        yield (r_idx, c_idx)
                else: #完全一致
                    if value == field:
                        yield (r_idx, c_idx)

    def get_field_value(self, row_idx, col_idx):
        """
        TwoDimArrayにインデックスでアクセスしてその値を返す
        """
        value = self.data[row_idx][col_idx]
        return value

    def inquire_field_value(self, row_value, col_value):
        """
        行(フィールド値がrow_valueの行)と列(フィールド値がcol_valueの列)が交差するフィールド値を返す
        """
        row_idxs = [row_idx for row_idx, col_idx in self.get_field_idx_all(row_value)]
        col_idxs = [col_idx for row_idx, col_idx in self.get_field_idx_all(col_value)]
        if not row_idxs or not col_idxs:
            return None
        lengths = (len(row_idxs), len(col_idxs))

        field_values = [self.get_field_value(row_idx, col_idx) for row_idx, col_idx in product(row_idxs, col_idxs)]
        if all(length==1 for length in lengths):
            return field_values[0]
        elif any(length==1 for length in lengths):
            return field_values
        else:
            #row_idxs、col_idxsが共に複数ある場合は行毎に分ける
            return [field_values[i:i+len(col_idxs)] for i in range(len(field_values))[::len(col_idxs)]]

    #------------------------------
    # フィールド変換
    #------------------------------
    def field2striped_str(self):
        """
        文字列フィールドの左右の空白を削除(strip)
        """
        self.data = _field2striped_str(self.data)

    def field2int(self):
        """
        フィールドをintに変換できたらintに変換する
        """
        self.data = [[_chg_int(field) for field in row] for row in self.data]

    def field2float(self):
        """
        フィールドをfloatに変換できたらfloatに変換する
        """
        self.data = [[_chg_float(field) for field in row] for row in self.data]

    def money2int(self):
        """
        フィールドの通貨文字列をintに変換できたらintに変換する
        """
        self.data = [[_chg_money2int(field) for field in row] for row in self.data]

    def money2float(self):
        """
        フィールドの通貨文字列をfloatに変換できたらfloatに変換する
        """
        self.data = [[_chg_money2float(field) for field in row] for row in self.data]

    def refresh_field(self):
        """
        各フィールドをリフレッシュさせる
            各フィールドを文字列に変換、文字列の左右の空白を削除(strip)、intに変換できる文字列はintに、floatに変換できる文字列はfloatに変換する
        """
        self.data = [[_str2int_or_float(field) for field in row] for row in _field2striped_str(self.data)]

    def replace_field(self, before_value, after_value):
        """
        before_valueのフィールドをafter_valueにする
        """
        self.data = [[after_value if field == before_value else field for field in row] for row in self.data]

    def resub_field(self, pattern, repl):
        """
        各フィールドをre.sub(pattern, repl)したTwoDimArrayインスタンスを返す
            フィールドは文字列に変換してからre.sub関数で評価される
        """
        chg_tda = self.map_field(lambda field: re.sub(pattern, repl, str(field)))
        chg_tda.refresh_field() #re.subのために各フィールドを文字列に変換したので、元に戻す
        chg_tda._copy_property(self)
        return chg_tda

    def research_field(self, pattern):
        """
        各フィールドをre.search(pattern, field)してヒットしたfield値以外は空('')にしたTwoDimArrayインスタンスを返す
            フィールドは文字列に変換してからre.search関数で評価される
        """
        chg_tda = self.map_field(lambda field: field if re.search(pattern, str(field)) else '')
        chg_tda._copy_property(self)
        return chg_tda

    def split_multiplelines(self, multiplelines_field):
        """
        multiple-linesフィールドをデリミタ(self.multiple_lines_delimiter)で分割し、
        各要素をintやfloatに変換可能ならば変換したリストを返す
        """
        return [_str2int_or_float(field) for field in multiplelines_field.split(self.multiple_lines_delimiter)]

    def join_multiplelines(self, lst):
        """
        リストの各フィールド値をデリミタ(self.multiple_lines_delimiter)で結合した文字列を返す
        """
        return self.multiple_lines_delimiter.join(map(str, lst))

    #------------------------------
    # column操作
    #------------------------------
    def get_column(self, col_idx):
        """
        指定された列をコピーして返す
            col_idxはsliceも指定可能
        """
        columns = row2column(self.data)
        try:
            column = columns[col_idx]
        except IndexError:
            return None

        return column

    def del_column(self, col_idx):
        """
        指定された列の削除
            col_idxはsliceも指定可能
        """
        columns = row2column(self.data)
        try:
            del(columns[col_idx])
        except IndexError:
            pass

        self.data = row2column(columns)

    def remove_column(self, col_idx):
        """
        指定された列を抜き出す
            col_idxはsliceも指定可能
        """
        column = self.get_column(col_idx)
        self.del_column(col_idx)

        return column

    def chg_column(self, col_idx, new_column):
        """
        指定された列をnew_columnに置き換える
        """
        self.del_column(col_idx)
        self.add_column(col_idx, new_column)

    def chg_colidx(self, col_idx1, col_idx2):
        """
        col_idx1の列とcol_idx2の列を入れ替える
        """
        col1 = self.get_column(col_idx1)
        col2 = self.get_column(col_idx2)

        if col1:
            self.chg_column(col_idx2, col1) #col1の列がcol2のあった場所に入る
        else:
            self.del_column(col_idx2) #col1が無いので、col2の列が移動して元の場所から消える

        if col2:
            self.chg_column(col_idx1, col2) #col2の列がcol1のあった場所に入る
        else:
            self.del_column(col_idx1) #col2が無いので、col1の列が移動して元の場所から消える

    def add_column(self, col_idx, new_column):
        """
        列データ(new_column)をTwoDimArray(self.data)の指定インデックス(col_idx)に追加する
            col_idxがNoneならば列データをTwoDimArrayの最後尾に追加する
        """
        columns = row2column(self.data) #行と列の入れ替え
        columns = self._add_column(columns, col_idx, new_column)
        self.data = row2column(columns) #再び行と列の入れ替えをして元に戻す

    def extend_columns(self, col_idx, new_columns):
        """
        TwoDimArray(self.data)を列データ(new_columns)で拡張する
            col_idxで指定したインデックスから拡張する
            col_idxがNoneならばTwoDimArrayの最後尾から拡張する
        """
        columns = row2column(self.data) #行と列の入れ替え

        for idx, new_column in enumerate(new_columns):
            if col_idx is None:
                columns = self._add_column(columns, None, new_column) #最後尾に追加する
            else:
                columns = self._add_column(columns, col_idx+idx, new_column)

        self.data = row2column(columns) #再び行と列の入れ替えをして元に戻す

    def _add_column(self, columns, col_idx, new_column):
        """
        columnsのcol_idxにnew_columnを追加する(add_columnとextend_columnsの共通処理)
            col_idxがNoneならばcolumnsの最後尾に追加する
        """
        if col_idx is None: #Noneならば最後尾に追加する
            col_idx = len(columns)

        new_column = [_str2striped_str(field) for field in new_column] #文字列のフィールドをstrip()して左右の空白削除
        new_column = [_str2int_or_float(field) for field in new_column] #intに変換できる文字列はintに、floatに変換できる文字列はfloatに変換

        if col_idx <= len(columns) - 1: #col_idxがself.dataの範囲内の場合
            #print(f'col_idx: {col_idx}, len(columns)-1: {len(columns)-1}') ###
            columns.insert(col_idx, new_column)
        else:
            blank_col_num = col_idx - len(columns)
            blank_col = ('',) * max([len(col) for col in columns])
            #print(f'blank_col_num: {blank_col_num}'); print(f'blank_col: {blank_col}') ###

            columns += [blank_col,]*blank_col_num #ブランク追加
            columns.append(new_column)

        return columns

    def arrange_columns(self, *col_idxs):
        """
        列のインデックスの並び(col_idxs)の通りにTwoDimArrayを再構築したTwoDimArrayインスタンスを返す
        """
        columns = row2column(self.data)
        tda_data = row2column([columns[col_idx] for col_idx in col_idxs if col_idx <= len(columns)-1])
        if not tda_data:
            tda_data = [['']]

        new_tda = TwoDimArray(tda_data)
        new_tda._copy_property(self)
        return new_tda
        
    #------------------------------
    # row操作
    #------------------------------
    def arrange_rows(self, *row_idxs):
        """
        行のインデックスの並び(row_idxs)の通りにTwoDimArrayを再構築したTwoDimArrayインスタンスを返す
        """
        tda_data = [self.data[row_idx] for row_idx in row_idxs if row_idx <= len(self.data)-1]
        if not tda_data:
            tda_data = [['']]

        new_tda = TwoDimArray(tda_data)
        new_tda._copy_property(self)
        return new_tda

    #------------------------------
    # 高度な操作
    #------------------------------
    @set_row_range
    def sort(self, key=None, reverse=False, row_start_idx=0, row_end_idx=None):
        """
        行範囲[row_start_idx:row_end_idx]の各行をsortする
        """
        self.data = [*self.data[0:row_start_idx],
                    *sorted(self.data[row_start_idx:row_end_idx], key=key, reverse=reverse),
                    *([] if row_end_idx is None else self.data[row_end_idx:])
                    ]

    @set_row_range
    def fill(self, fillvalue='', row_start_idx=0, row_end_idx=None):
        """
        行範囲[row_start_idx:row_end_idx]内の行列で欠けている箇所をfillvalueで埋める
        """
        tda_data = [*self.data[0:row_start_idx],
                    *[list(row) for row in zip_longest(*zip_longest(*self.data[row_start_idx:row_end_idx], fillvalue=fillvalue))],
                    *([] if row_end_idx is None else self.data[row_end_idx:])
                    ]
        self.data = tda_data

    def trim(self, row=True, col=True):
        """
        空の行、空の列を除去する
            文字列のフィールドはstripしてから空判定する
        """
        if row:
            not_empty_row_idx = [row_idx for row_idx, row in enumerate(self.data) if any([field.strip() if isinstance(field, str) else field for field in row])]
            if len(not_empty_row_idx) != len(self.data):
                new_tda = self.arrange_rows(*not_empty_row_idx)
                self.data = new_tda.data

        if col:
            columns = row2column(self.data)
            not_empty_col_idx = [col_idx for col_idx, col in enumerate(columns) if any([field.strip() if isinstance(field, str) else field for field in col])]
            if len(not_empty_col_idx) != len(columns):
                new_tda = self.arrange_columns(*not_empty_col_idx)
                self.data = new_tda.data

    @set_row_range
    def filter(self, func=None, row_start_idx=0, row_end_idx=None):
        """
        行範囲[row_start_idx:row_end_idx]の各行をfilterしたTwoDimArrayインスタンスを返す
        """
        tda_data = [*self.data[0:row_start_idx],
                    *filter(func, self.data[row_start_idx:row_end_idx]),
                    *([] if row_end_idx is None else self.data[row_end_idx:])
                    ]
        new_tda = TwoDimArray(tda_data)
        new_tda._copy_property(self)
        return new_tda

    @set_row_range
    def map_field(self, func=None, row_start_idx=0, row_end_idx=None):
        """
        行範囲[row_start_idx:row_end_idx]の各フィールド値をmapしたTwoDimArrayインスタンスを返す
            funcの引数には各フィールド値が渡される
            funcがエラーになる場合は空文字('')を返す
        """
        if self.multiple_lines:
            func = Wrapper.support_multiplelines(func, self.multiple_lines_delimiter)
        func = Wrapper.non_error(func) #func処理でエラーなら''を返すラッパー関数

        tda_data = [*self.data[0:row_start_idx],
                    *[list(map(func, row)) for row in self.data[row_start_idx:row_end_idx]],
                    *([] if row_end_idx is None else self.data[row_end_idx:])
                    ]
        new_tda = TwoDimArray(tda_data)
        new_tda._copy_property(self)
        return new_tda

    @set_row_range
    def map_rows(self, func=None, row_start_idx=0, row_end_idx=None):
        """
        self.dataの各行をmapした配列を返す
            funcがエラーになる場合は空文字('')を返す
        """
        if self.multiple_lines:
            func = Wrapper._arg_of_flatten_multiplelines_list(func, self.multiple_lines_delimiter)
        func = Wrapper.non_error(func)

        top = ['' for _ in range(len(self.data[0:row_start_idx]))]
        bottom = [] if row_end_idx is None else ['' for _ in range(len(self.data[row_end_idx:]))]
        return top + list(map(func, self.data[row_start_idx:row_end_idx])) + bottom

    @set_row_range
    def map_columns(self, func=None, row_start_idx=0, row_end_idx=None):
        """
        self.dataの各列をmapした配列を返す
            funcがエラーになる場合は空文字('')を返す
        """
        if self.multiple_lines:
            func = Wrapper._arg_of_flatten_multiplelines_list(func, self.multiple_lines_delimiter)
        func = Wrapper.non_error(func)

        return list(map(func, row2column(self.data[row_start_idx:row_end_idx])))

    @set_row_range
    def cal_columns(self, col_idxs, func=None, row_start_idx=0, row_end_idx=None):
        """
        各列間のfunc処理の結果を返す
            各列の同じ行の値がfuncに入力され、その処理結果を収めた配列を返す
            funcがエラーになる場合は空文字('')を返す
        """
        if self.multiple_lines:
            func = Wrapper.support_multiplelines(func, self.multiple_lines_delimiter)
        func = Wrapper.non_error(func) #func処理でエラーなら''を返すラッパー関数

        if not hasattr(col_idxs, '__iter__'): #指定インデックスが1つのみの場合
            col_idxs = (col_idxs,)

        columns = [self.get_column(col_idx)[row_start_idx:row_end_idx] for col_idx in col_idxs]
        args = row2column(columns)

        top = ['' for _ in range(len(self.data[0:row_start_idx]))]
        bottom = [] if row_end_idx is None else ['' for _ in range(len(self.data[row_end_idx:]))]
        return top + [func(*arg) for arg in args] + bottom

    def row2column(self):
        """
        TwoDimArrayの行と列を入れ替える
        """
        self.data = row2column(self.data)

    def tda2list(self):
        """
        2次元リストのTwoDimArrayを1次元リストに変換する
        """
        return [j for i in self.data for j in i]

    def rotate_l45(self):
        """
        TwoDimArrayを左に45度回転させる
        """
        row_len = self._row_len()

        self.rotate_l90()
        self.data = [['']*col_idx+col for col_idx, col in enumerate(self.data)]
        self.rotate_r90()
        [row.append('') if -row_idx+slit_idx >= 0 else row.insert(-row_idx+slit_idx, '') for row_idx, row in enumerate(self.data)
         for slit_idx in range(row_len-1)] #右斜め下にフィールド値を移動
        self.trim()

    def rotate_r45(self):
        """
        TwoDimArrayを右に45度回転させる
        """
        row_len = self._row_len()

        self.row2column()
        self.data = [['']*col_idx+col for col_idx, col in enumerate(self.data)]
        self.row2column()
        [row.insert(0, '') if row_idx-slit_idx <= 0 else row.insert(row_idx-slit_idx, '') for row_idx, row in enumerate(self.data)
         for slit_idx in range(row_len-1)] #左斜め下にフィールド値を移動
        self.trim()

    def rotate_l90(self):
        """
        TwoDimArrayを左に90度回転させる
        """
        self.row2column()
        self.data = self.data[::-1]

    def rotate_r90(self):
        """
        TwoDimArrayを右に90度回転させる
        """
        self.row2column()
        self.data = [row[::-1] for row in self.data]

    def invert_x(self):
        """
        x軸で反転
        """
        self.data = self.data[::-1]

    def invert_y(self):
        """
        y軸で反転
        """
        self.data = [row[::-1] for row in self.data]

    def invert_xy(self):
        """
        x軸で反転 and y軸で反転
        """
        self.invert_x()
        self.invert_y()

    def invert_slash(self):
        """
        斜め(スラッシュ)軸で反転
        """
        self.row2column()
        self.invert_xy()

    def invert_bslash(self):
        """
        斜め(バックスラッシュ)軸で反転
        """
        self.row2column()
        self.rotate_r90(); self.rotate_r90();
        self.invert_xy()

    def get_slash(self):
        """
        斜め(スラッシュ)軸要素を新しいTwoDimArrayインスタンスとして返す
        """
        row_len = self._row_len()
        tda_data = [[field if abs(field_idx+row_idx)==row_len-1 else ''  for field_idx, field in enumerate(row)]
                    for row_idx, row in enumerate(self.data)]
        new_tda = TwoDimArray(tda_data)
        new_tda._copy_property(self)
        return new_tda

    def get_bslash(self):
        """
        斜め(バックスラッシュ)軸要素を新しいTwoDimArrayインスタンスとして返す
        """
        tda_data = [[field if field_idx==row_idx else ''  for field_idx, field in enumerate(row)]
                    for row_idx, row in enumerate(self.data)]
        new_tda = TwoDimArray(tda_data)
        new_tda._copy_property(self)
        return new_tda

    def get_diagonal(self):
        """
        TwoDimArrayの対角線要素を新しいTwoDimArrayインスタンスとして返す
        """
        return self.get_slash() + self.get_bslash()

    def get_slash_stripe(self):
        """
        ストライプ(スラッシュ方向)要素を新しいTwoDimArrayインスタンスとして返す
        """
        tda_data = [[field if (field_idx+row_idx)%2==1 else ''  for field_idx, field in enumerate(row)]
                    for row_idx, row in enumerate(self.data)]
        new_tda = TwoDimArray(tda_data)
        new_tda._copy_property(self)
        return new_tda

    def get_bslash_stripe(self):
        """
        ストライプ(バックスラッシュ方向)要素を新しいTwoDimArrayインスタンスとして返す
        """
        tda_data = [[field if (field_idx+row_idx)%2==0 else ''  for field_idx, field in enumerate(row)]
                    for row_idx, row in enumerate(self.data)]
        new_tda = TwoDimArray(tda_data)
        new_tda._copy_property(self)
        return new_tda

    #------------------------------
    # データ集計
    #------------------------------
    @set_row_range
    def groupby(self, grouping_col_idxs, target_col_idxs=None, func=None, row_start_idx=0, row_end_idx=None):
        """
        選択した列のフィールド値でグループ化し集計したTwoDimArrayインスタンスを返す
            grouping_col_idxs: グループ化対象の列
            target_col_idxs: 集計対象の列(Noneならgrouping_col_idxs以外の全ての列)
            func: 集計関数(target_col_idxsを集計する関数)
                  funcがエラーになる場合は空文字('')を返す
        """
        if func is None:
            func = lambda fields: self.multiple_lines_delimiter.join(map(str, fields))

        if not hasattr(grouping_col_idxs, '__iter__'): #指定インデックスが1つのみの場合
            grouping_col_idxs = (grouping_col_idxs,)

        if target_col_idxs is None: #grouping_col_idxs以外のインデックス全部
            col_set = {*range(self.shape()[1])}
            group_set = {*grouping_col_idxs}
            if len(col_set) >= len(group_set):
                target_col_idxs = col_set - group_set
            else:
                target_col_idxs = group_set - col_set
        elif not hasattr(target_col_idxs, '__iter__'): #指定インデックスが1つのみの場合
            target_col_idxs = (target_col_idxs,)

        #tupleに統一
        grouping_col_idxs = tuple(grouping_col_idxs)
        target_col_idxs = tuple(target_col_idxs)
        #print(f'grouping_col_idxs: {grouping_col_idxs}') ###
        #print(f'target_col_idxs: {target_col_idxs}') ###

        group_dict = defaultdict(list)
        add_group_dict = lambda key, value: group_dict[key].append(value)
        group_len = len(grouping_col_idxs)
        self.cal_columns(grouping_col_idxs+target_col_idxs,
                         lambda *args: add_group_dict(args[:group_len], args[group_len:]),
                         row_start_idx=row_start_idx, row_end_idx=row_end_idx)
        #print(group_dict) ###

        func = Wrapper.non_error(func) #func処理でエラーなら''を返すラッパー関数
        arranged_tda = self.arrange_columns(*(grouping_col_idxs+target_col_idxs))
        new_tda = TwoDimArray([*arranged_tda.data[0:row_start_idx],
                               *[list(key)+[_str2int_or_float(func(args)) for args in zip(*value)] for key, value in group_dict.items()],
                               *([] if row_end_idx is None else arranged_tda.data[row_end_idx:])])

        new_tda._copy_property(self)
        return new_tda

    @set_row_range
    def cross_count(self, col_idx1, col_idx2, row_start_idx=0, row_end_idx=None, field_fmt='{count} ({percent}%)'):
        """
        選択した2列(col_idx1, col_idx2)をクロス集計したTwoDimArrayインスタンスを返す
        集計内容はカウント数とパーセント値、表示形式はfield_fmtで設定できる
            col_idx1: クロス集計するTwoDimArrayの行(header)となる
            col_idx2: クロス集計するTwoDimArrayの列(左端列)となる
        """
        target_tda = self.arrange_columns(col_idx1, col_idx2)
        counter = Counter([tuple(row) for row in target_tda.data[row_start_idx:row_end_idx]])
        total_num = sum(counter.values())

        rows, cols = zip(*counter.keys())
        rows = sorted(set(rows))
        cols = sorted(set(cols))

        def get_field(key):
            count = counter[key]
            percent = f'{count/total_num*100:.0f}'
            return _chg_int(field_fmt.format(count=count, percent=percent))

        new_tda = TwoDimArray([rows] + [[get_field((row, col)) for row in rows] for col in cols])
        new_tda.add_column(0, [''] + cols) #rowsを追加した分ブランク['']を追加

        new_tda._copy_property(self)
        return new_tda

    @set_row_range
    def describe(self, func_lst=(len, max, min, sum, mean, median, variance, stdev), row_start_idx=0, row_end_idx=None):
        """
        func_lstに設定した各集計関数で各列を集計したTwoDimArrayインスタンスを返す
            集計関数には列データの内、数字のデータのみが渡る
        """
        if self.header_idx is None:
            header = []
        else:
            header = [[''] + self.data[self.header_idx]]

        new_tda = TwoDimArray(header + [[func.__name__] + self.map_columns(Wrapper.arg_of_numlist(func)) for func in func_lst])
        new_tda._copy_property(self)
        return new_tda

    #------------------------------
    # 枠
    #------------------------------
    def wrap_border(self, border_pattern=None, header_aligns=None, aligns=None, widths=None):
        """
        self.dataを枠で囲んだTwoDimArrayインスタンスを返す
            ・border_pattern: 枠パターン(border_patternsの中から選択)

            各列の書式指定を個別に指定できる:
                ・header_aligns: ヘッダーのalignを設定する辞書{列インデックス: align} (align: 左詰め='<'、右詰め='>', 中央寄せ='^')
                ・aligns: 各列のalignを設定する辞書{列インデックス: align} (align: 左詰め='<'、右詰め='>', 中央寄せ='^')
                ・widths: 各列のwidthを設定する辞書{列インデックス: width}
            ※列インデックスで指定されていない他の全ての設定をNoneキーで設定できる
        """
        #枠パターン取得
        if border_pattern is None:
            p = border_patterns.get(self.print2_border)
        else:
            p = border_patterns.get(border_pattern)

        if p is None:
            return
        p_tda = TwoDimArray([[char for char in row] for row in p.strip('\n').split('\n')]) #枠パターンを参照するTwoDimArray
        p_tda._display_delimiter = '' #枠の表示が崩れないように表示用デリミタを空にする(デバッグ用)
        #p_tda.print() ###

        #TwoDimArrayをコピー & データに穴があれば埋める
        columns = row2column(self.data)
        data = row2column(columns)
        d_tda = TwoDimArray(data)
        d_tda._copy_property(self)

        #枠パターンの行数を増減(d_tdaの行が入るよう)
        if p_tda._row_len()//2 == d_tda._row_len(): #同じ大きさ
            pass
        elif p_tda._row_len()//2 > d_tda._row_len(): #d_tdaが枠パターンより小さい
            del(p_tda.data[d_tda._row_len()*2: -1])
        else: #d_tdaが枠パターンより大きい
            p_columns = row2column(p_tda.data)
            row_increase = d_tda._row_len() - p_tda._row_len()//2
            p_center = {'row': p_tda._row_center(), 'col': p_tda._col_center()} #初期値(行を増加させる前の値を確保)
            #print(f'row_increase: {row_increase}') ###
            for col_idx in range(p_tda._col_len()):
                L = p_columns[col_idx][p_center['row']-1: p_center['row']+1][::-1]
                L = L*(row_increase//2 + row_increase%2)
                R = p_columns[col_idx][p_center['row']: p_center['row']+2][::-1]
                R = R*(row_increase//2)
                #print(f'row: L:{L}, R:{R}') ###
                C = L + [p_columns[col_idx][p_center['row']]] + R
                p_columns[col_idx] = p_columns[col_idx][:p_center['row']] + C + p_columns[col_idx][p_center['row']+1:]
            p_tda.data = row2column(p_columns)
        #p_tda.print() ###
        #print(f'p_tda len 2: {p_tda._row_len()}, {p_tda._col_len()}') ###

        #枠パターンの列数を増減(d_tdaの列が入るよう)
        if p_tda._col_len()//2 == d_tda._col_len(): #同じ大きさ
            pass
        elif p_tda._col_len()//2 > d_tda._col_len(): #d_tdaが枠パターンより小さい
            p_columns = row2column(p_tda.data)
            del(p_columns[d_tda._col_len()*2: -1])
            p_tda.data = row2column(p_columns)
        else: #d_tdaが枠パターンより大きい
            col_increase = d_tda._col_len() - p_tda._col_len()//2
            p_center = {'row': p_tda._row_center(), 'col': p_tda._col_center()} #初期値(列を増加させる前の値を確保)
            #print(f'col_increase: {col_increase}') ###
            for row_idx in range(p_tda._row_len()):
                L = p_tda.data[row_idx][p_center['col']-1: p_center['col']+1][::-1]
                L = L*(col_increase//2 + col_increase%2)
                R = p_tda.data[row_idx][p_center['col']: p_center['col']+2][::-1]
                R = R*(col_increase//2)
                #print(f'col: L:{L}, R:{R}') ###
                C = L + [p_tda.data[row_idx][p_center['col']]] + R
                p_tda.data[row_idx] = p_tda.data[row_idx][:p_center['col']] + C + p_tda.data[row_idx][p_center['col']+1:]
        #p_tda.print() ###
        #print(f'p_tda len 3: {p_tda._row_len()}, {p_tda._col_len()}') ###

        #枠のグループ化(隣接するフィールド値が同じならば、その境界の枠をスペースにする)
        if self.border_grouping:
            #隣接する各フィールド値が同じ値か否かの情報生成
            col_diff = [[field != next_field for field, next_field in zip(row[:-1], row[1:])] for row in d_tda.data]
            row_diff = [[field != next_field for field, next_field in zip(col[:-1], col[1:])] for col in columns]
            row_diff = row2column(row_diff)
            #print(f'col_diff: {repr(col_diff)}') ###
            #print(f'row_diff: {repr(row_diff)}') ###
            #if col_diff and col_diff[0]: col_diff_tda = TwoDimArray(col_diff); print('col_diff:\n'); col_diff_tda.print() ###
            #if row_diff and row_diff[0]: row_diff_tda = TwoDimArray(row_diff); print('row_diff:\n'); row_diff_tda.print() ###

            for row_idx, row_data in enumerate(col_diff):
                for idx, diff in enumerate(row_data):
                    if not diff:
                        p_tda.data[row_idx*2+1][idx*2+2] = ' '

            for row_idx, row_data in enumerate(row_diff):
                for idx, diff in enumerate(row_data):
                    if not diff:
                        p_tda.data[row_idx*2+2][idx*2+1] = ' '
            #p_tda.print() ###

        #multiple-lines
        if self.multiple_lines:
            new_d_tda, new_p_tda = d_tda._extend_multiple_lines(p_tda)
            d_tda = d_tda if new_d_tda is None else new_d_tda
            p_tda = p_tda if new_p_tda is None else new_p_tda
            columns = row2column(d_tda.data)
            #d_tda.print() ###
            #p_tda.print() ###

        #alignとwidthを適用した文字列生成
        #width設定
        col_max_widths = _max_widths(columns, grouping_opt=self.grouping_opt, precision=self.precision)
        #print(f'col_max_widths: {col_max_widths}') ###
        if widths is not None and isinstance(widths, dict):
            other_width = widths.get(None)
            if other_width:
                c_widths = defaultdict(lambda:other_width)
            else:
                c_widths = defaultdict(lambda:0)
            c_widths.update(widths)
            col_max_widths = [c_widths[col_idx] if c_widths[col_idx] > col_max_width else col_max_width
                              for col_idx, col_max_width in enumerate(col_max_widths)] #widthsを取り込む(大きい値を採用)
            #print(f'col_max_widths: {col_max_widths}(カスタム化)') ###
        col_max_widths = [width if width%2 == 0 else width+1 for width in col_max_widths] #文字幅2のフィールド値や枠にも対応できるようにwidthを偶数にする
        #print(f'col_max_widths: {col_max_widths}') ###
        widths = dict([(i, w) for i,w in enumerate(col_max_widths)])

        d_tda._display_delimiter = ','
        fields_str = d_tda._fields_string_format(header_aligns=header_aligns, aligns=aligns, widths=widths)
        d_tda = TwoDimArray([[field for field in row] for row in fields_str]) #TwoDimArray化(alignとwidth情報を消さないように各フィールドはstripしない)
        #d_tda.print() ###

        #p_tdaにd_tdaの値を入れる
        for row_idx, row_data in enumerate(p_tda.data):
            for idx, p_field in enumerate(row_data):
                if idx % 2 == 1:
                    if row_idx % 2 == 0:
                        col_max_width = col_max_widths[idx//2]
                        if _is_em(p_field):
                            p_tda.data[row_idx][idx] = p_field * (col_max_width//2) #各列の文字幅に合うように枠の数を調整
                        else:
                            p_tda.data[row_idx][idx] = p_field * col_max_width #各列の文字幅に合うように枠の数を調整
                    else:
                        p_tda.data[row_idx][idx] = d_tda.data[row_idx//2][idx//2] #p_tdaにd_tdaの値を入れる

        p_tda._copy_property(self)
        p_tda._display_delimiter = '' #枠の表示が崩れないように表示用デリミタを空にする
        p_tda.trim(row=True, col=False) #空白の枠の行を削除する
        return p_tda

#------------------------------
# 公開関数
#------------------------------
def load(csv_file, sep=',', encoding=None):
    """
    csvファイル(csv_file)からTwoDimArrayを作成
        sep: セパレータは正規表現も指定可能
    """
    with open(csv_file, encoding=encoding) as f:
        return _file_obj2tda(f, sep=sep)

def csv2tda(string, sep=','):
    """
    csvの文字列をTwoDimArrayに変換する
        sep: セパレータは正規表現も指定可能
    """
    return _file_obj2tda(io.StringIO(string), sep=sep)

def df2tda(df, index=False, **kwargs):
    """
    pandasのDataFrameをTwoDimArrayに変換する
    """
    if hasattr(df, 'to_csv') and inspect.ismethod(df.to_csv):
        try:
            csv = df.to_csv(index=index, **kwargs)
        except:
            return
    return csv2tda(csv)

def list2tda(lst, col_num):
    """
    1次元リストを2次元リストのTwoDimArrayに変換する
    """
    return TwoDimArray([lst[i:i+col_num] for i in range(len(lst))[::col_num]])

def dict2tda(dct):
    """
    辞書をTwoDimArrayに変換する
        辞書の各アイテムは列とする
    """
    new_tda = TwoDimArray([[key]+list(value) if hasattr(value, '__iter__') and not isinstance(value, str) else [key]+[value]
                          for key, value in dct.items()])
    new_tda.row2column()
    return new_tda

def str2list(string):
    """
    文字列をカンマで区切った配列に変換する
        カンマで区切ったフィールドはstripしてintに変換できたらint、floatに変換できたらfloatに変換する
    """
    return [_str2int_or_float(field.strip()) for field in string.split(',')]

def list2str(lst):
    """
    リストを文字列に変換する
    """
    return ', '.join([str(i) for i in lst])

def row2column(tda_data):
    """
    行と列を入れ替える
    """
    return [list(row) for row in zip_longest(*tda_data, fillvalue='')] #zip_longestによってタプルになった要素をリストに戻す

def chk_border():
    """
    TwoDimArrayを囲む枠のパターン(border_patterns)を表示する
    """
    for key, pattern in border_patterns.items():
        print(f'border_pattern: {repr(key)}\n{pattern}\n')

#------------------------------
# 非公開関数
#------------------------------
def _file_obj2tda(fileObj, sep=','):
    """
    ファイルオブジェクトからTwoDimArrayを読み出す
        sep: セパレータは正規表現も指定可能
    """
    re_sep = re.compile(sep)
    tda_data = [[field.strip() for field in re_sep.split(row.strip())] for row in fileObj] #フィールドをsepで区切り、各フィールドをstrip()
    tda_data = _str_field2int_or_float(tda_data) #intに変換できる文字列はintに、floatに変換できる文字列はfloatに変換
    tda = TwoDimArray(tda_data)
    if hasattr(fileObj, 'name'): #ファイルからデータを読み込んだ場合はファイル名が取得できる
        tda.name = fileObj.name
    else:
        tda.name = ''
    return tda

#文字幅関係------------------------------
def _max_widths(columns, grouping_opt=False, precision=6):
    """
    各列の最大文字列幅を返す
    """
    columns = _field2str(columns, grouping_opt, precision)
    return [max([_width(field) for field in col]) for col in columns]

def _width(string):
    """
    全角文字の文字幅を2として文字列幅を算出する
    """
    return sum([2 if _is_em(char) else 1 for char in string])

def _count_em(string):
    """
    全角文字の文字数を返す
    """
    return sum([1 for char in string if _is_em(char)])

en_table = [
'═', '║', '╔','╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬', #Double
'·', '╭', '╮', '╯', '╰', #Rcorner
'♠', '♥', '♦', '♣', '♤', '♡', '♢', '♧', #Suit
]

def _is_em(char):
    """
    全角文字ならTrueを返す
    """
    #------------------------------------------------------------
    #文字判定: F: Fullwidth(全角) - 全角英数字
    #          W: Wide(広) - 漢字や仮名文字など
    #          A: Ambiguous(曖昧) - 記号など(全角/半角が交じっている)
    #
    # ※使いたい枠(罫線)がAグループなのでAも全角文字として扱う
    #   このためAグループの半角文字を使用した場合は誤判定して
    #   位置ズレの原因となるため注意すること
    #   (Aグループでもen_tableに登録した文字は半角として判定する)
    #------------------------------------------------------------
    data = unicodedata.east_asian_width(char)
    if data in ('F', 'W'):
        return True
    elif data in ('A',) and char not in en_table:
        return True

    return False

#フィールド変換------------------------------
def _field2str(tda_data, grouping_opt=False, precision=6):
    """
    TwoDimArrayのフィールドを全て文字列に変える
        grouping_opt: 数字の区切り文字アンダースコアの有無
        precision: floatの精度
    """
    grouping_option = ''
    if grouping_opt:
        grouping_option = '_'

    return [[f'{field:{grouping_option}}' if isinstance(field, int) else f'{field:{grouping_option}.{precision}f}' if isinstance(field, float) else str(field) for field in row]
            for row in tda_data]

def _field2striped_str(tda_data):
    """
    TwoDimArrayのフィールドを全てstripした文字列に変える
    """
    return [[_chg_striped_str(field) for field in row] for row in tda_data]

def _str_field2int_or_float(tda_data):
    """
    TwoDimArrayのフィールドでintに変換できる文字列はintに、floatに変換できる文字列はfloatに変換
    """
    return [[_str2int_or_float(field) for field in row] for row in tda_data]

#文字列変換------------------------------
def _str2striped_str(string):
    if isinstance(string, str):
        return string.strip()

    return string

def _str2int(string):
    if isinstance(string, str) and string:
        string = _chg_int(string)

    return string

def _str2float(string):
    if isinstance(string, str) and string:
        string = _chg_float(string)

    return string

def _str2int_or_float(string):
    """
    文字列からintに変換できたらintに、文字列からfloatに変換できたらfloatに変換する
    """
    if isinstance(string, str):
        string = _str2int(string)

    if isinstance(string, str):
        string = _str2float(string)

    return string

#変換------------------------------
def _chg_striped_str(something):
    return str(something).strip()

def _chg_int(something):
    """
    intに変換できたらintに変換する
    """
    try:
        i = int(something)
        return i
    except ValueError:
        pass

    return something

def _chg_float(something):
    """
    floatに変換できたらfloatに変換する
    """
    try:
        f = float(something)
        return f
    except ValueError:
        pass

    return something

# ﾊﾞｯｸｽﾗｯｼｭはchr(92)とchr(165)がありファイルから読み込んだ時は\\ == chr(92)、IDLEで入力/コピペした時はchr(92)やchr(165)になる
money = re.compile(rf'^[{chr(165)}\\$0-9.,]+$')
del_money_symbol = rf'{chr(165)}\\$,'
def _chg_money2int(something):
    """
    通貨文字列をintに変換できたらintに変換する
    """
    if money.match(something):
        return _chg_int(something.translate(str.maketrans('', '', del_money_symbol)))
    else:
        return something

def _chg_money2float(something):
    """
    通貨文字列をfloatに変換できたらintに変換する
    """
    if money.match(something):
        return _chg_float(something.translate(str.maketrans('', '', del_money_symbol)))
    else:
        return something

#--------------------------------------------------------------------------------
# 枠パターン
#--------------------------------------------------------------------------------
#   行列の数に合わせてパターンの中心線xyから枠が増殖するイメージ
#
#                y                        y                        y
#   pattern ┌ＡＢＣ┐           ┌ＡＢＡＢＣ┐           ┌ＡＢＡＢＣＢＣ┐
#           Ｄ　Ｅ　Ｆ   列増    Ｄ　Ｅ　Ｅ　Ｆ   列増    Ｄ　Ｅ　Ｅ　Ｅ　Ｆ
#         x ＧＨＩＪＫ  -----> x ＧＨＩＨＩＪＫ  -----> x ＧＨＩＨＩＪＩＪＫ
#           Ｌ　Ｍ　Ｎ           Ｌ　Ｍ　Ｍ　Ｎ           Ｌ　Ｍ　Ｍ　Ｍ　Ｎ
#           └ＯＰＱ┘           └ＯＰＯＰＱ┘           └ＯＰＯＰＱＰＱ┘
#
#                                     y                    y
#                                ┌ＡＢＣ┐           ┌ＡＢＣ┐
#                 y              Ｄ　Ｅ　Ｆ           Ｄ　Ｅ　Ｆ
#   pattern  ┌ＡＢＣ┐          ＧＨＩＪＫ           ＧＨＩＪＫ
#            Ｄ　Ｅ　Ｆ  行増    Ｄ　Ｅ　Ｆ   行増    Ｄ　Ｅ　Ｆ
#          x ＧＨＩＪＫ -----> x ＧＨＩＪＫ  -----> x ＧＨＩＪＫ
#            Ｌ　Ｍ　Ｎ          Ｌ　Ｍ　Ｎ           Ｌ　Ｍ　Ｎ
#            └ＯＰＱ┘          └ＯＰＱ┘           ＧＨＩＪＫ
#                                                     Ｌ　Ｍ　Ｎ
#                                                     └ＯＰＱ┘
#                              
#
#   上記のように、列はpatternの中心線yの左の枠文字、右の枠文字と左右の順で使う
#                 行はpatternの中心線xの上の枠文字、下の枠文字と上下の順で使う
#
#   ※空白のみで構成された枠の行は最後に消される
#--------------------------------------------------------------------------------
border_patterns = {
#ascii
    'Grid': """
+-+-+
| | |
+=+=+
| | |
+-+-+
| | |
+-+-+
| | |
+-+-+
""",
    'Org': """
     
| | |
|-+-|
| | |
     
| | |
     
| | |
     
""",
    'Psql': """
+-+-+
| | |
+-+-+
| | |
     
| | |
     
| | |
+-+-+
""",
    'Rst': """
 = = 
     
 = = 
     
     
     
     
     
 = = 
""",
    'Simple': """
     
     
 - - 
     
     
     
     
     
     
""",
    'Standard': """
+-+-+
| | |
+-+-+
| | |
+-+-+
""",

#半角特殊文字
    'Rcorner': """
╭-·-╮
| | |
·-+-·
| | |
╰-·-╯
""",
    'Double': """
╔═╦═╗
║ ║ ║
╠═╬═╣
║ ║ ║
╚═╩═╝
""",

#全角特殊文字
    0: """
┌─┬─┐
│　│　│
├─┼─┤
│　│　│
└─┴─┘
""",
    1: """
┏━┳━┓
┃　┃　┃
┣━╋━┫
┃　┃　┃
┗━┻━┛
""",
    2: """
┏━┯━┓
┃　│　┃
┣━┿━┫
┃　│　┃
┠─┼─┨
┃　│　┃
┠─┼─┨
┃　│　┃
┗━┷━┛
""",
    3: """
┏━┳━┯━┯━┓
┃　┃　│　│　┃
┠─╂─┼─┼─┨
┃　┃　│　│　┃
┗━┻━┷━┷━┛
""",
    4: """
┏━┳━┯━┯━┓
┃　┃　│　│　┃
┣━╋━┿━┿━┫
┃　┃　│　│　┃
┠─╂─┼─┼─┨
┃　┃　│　│　┃
┠─╂─┼─┼─┨
┃　┃　│　│　┃
┗━┻━┷━┷━┛
""",
    5: """
┏━┳━┯━┳━┓
┃　┃　│　┃　┃
┣━╋━┿━╋━┫
┃　┃　│　┃　┃
┠─╂─┼─╂─┨
┃　┃　│　┃　┃
┣━╋━┿━╋━┫
┃　┃　│　┃　┃
┗━┻━┷━┻━┛
""",
    6: """
┏━┳━┓
┃　┃　┃
┠─╂─┨
┃　┃　┃
┗━┻━┛
""",
    7: """
┏━┯━┓
┃　│　┃
┣━┿━┫
┃　│　┃
┗━┷━┛
""",
    8: """
・～～～・
∫　∫　∫
∫～・～∫
∫　∫　∫
・～～～・
""",
    9: """
・～～～・
＼　∫　／
／～・～＼
＼　∫　／
　～～～　
""",
   10: """
・─・─・
│　│　│
・─・─・
│　│　│
・─・─・
""",

#print_idx2用(ascii)
    'Index': """
         
  : : :  
 .+-+-+. 
  | | |  
 .+-+-+. 
  | | |  
 .+-+-+. 
  : : :  
         
""",
    'Index_simple': """
         
         
   - -   
  |   |  
         
  |   |  
   - -   
         
         
""",

#テスト用
    'Test': """
ＡＢＣＤＥＦＧＨＩ
Ｊ　Ｋ　Ｌ　Ｍ　Ｎ
ＯＰＱＲＳＴＵＶＷ
Ｘ　Ｙ　Ｚ　あ　い
うえおかきくけこさ
し　す　せ　そ　た
ちつてとなにぬねの
は　ひ　ふ　へ　ほ
まみむめもやゆよわ
""",
}

