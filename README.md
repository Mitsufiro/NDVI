# NDVI
NDVI (Normalized Difference Vegetation Index) — нормализованный относительный индекс растительности — простой показатель количества фотосинтетически активной биомассы (обычно называемый вегетационным индексом). Этот индекс вычисляется по поглощению и отражению растениями лучей красной и ближней инфракрасной зоны спектра. Значения индекса для растительности лежат в диапазоне от 0,20 до 0,95. Чем лучше развита растительность во время вегетации, тем выше значение NDVI. Таким образом, NDVI – это индекс, по которому можно судить о развитии зеленой массы растений во время вегетации. 

Веб-сервис, который выгружает космические снимки и
определяет NDVI на поле, предоставляя REST API.

Снимки со спутника загружаются с помощью библиотеки sentinelsat в файле maps.py и далее используя различные каналы(инфракрасный и доинфракрасный диапазоны) космического снимка рассчитывается NDVI по формуле.

 ![alt text](https://github.com/Mitsufiro/NDVI/blob/main/zoomed_image.png)
 
 Достаточно просто загрузить geojson,можно посмотреть работу сервиса с помощью postman:
 
 ![alt text](https://github.com/Mitsufiro/NDVI/blob/main/from_postman.png)

Полезно сравнивать значения индекса вегетации (NDVI) ваших полей в разрезе нескольких лет. Это дает нужную информацию для формирования системы защиты и норм удобрений. Можно сравнить «сегодняшний» показатель NDVI со среднемноголетними значениями, сопоставить эти данные с урожайностью культур за прошлые годы (учёты прошлых лет) и спрогнозировать урожайность в текущем году. 

Но при оценке NDVI по спутниковым снимкам есть и минусы, которые скорее можно назвать небольшими недостатками при огромных достоинствах.
– У жителей туманного Лондона и не менее туманного Санкт-Петербурга могут возникнуть проблемы — высокая облачность не даст сделать спутнику хорошие снимки, а значит точно определить индекс вегетации и построить карты. Это значит, что индексная карта NDVI будет обновляться более редко, чем в степных южных регионах.
– На показатели индекса влияет густота посева и ширина междурядий, что особенно ярко проявляется в начале вегетации до смыкания рядков посевов.
– Карты NDVI не смогут полностью заменить выезды агронома на поля. Зато они отлично подскажут агроному, на какое поле нужно обратить более пристальное внимание. 
