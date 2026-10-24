# createCat.json
| key | val | description |
| -------- | -------- | -------- |
| ra | 259.212 | прямое восхождение RA центра поля |
| dec | 67.914 | склонение центра Dec поля |
| d_ra | 1 | диапазон поля по RA |
| d_dec | 0.35 | диапазон поля по Dec |

# createRefsCat.json
| key | val | description |
| -------- | -------- | -------- |
| Vcat_name | Vcat_F4.csv | название каталога с переменными |
| index_col | g_inx | поле с индексом |
| mag_st_max | 15 | максимальная зв.вел. для стандартных звезд |
| mag_st_min | 12 | минимальная зв.вел. для стандартных звезд |
| mag_high |12| граничная зв.вел. для условия mag < mag_high -> ro_min_hig |
| mag_low | 20 | граничная зв.вел. для условия (mag < mag_low) & (mag > mag_high ) -> ro_min_mid |


