from .models import (Stock,StockMarket,Debt,Choice)
import itertools
SAVING_CHOICES= [
('Altın/ONS','Altın/ONS'),
('Gümüş/ONS','Gümüş/ONS'),
('Altın/TL','Altın/TL'),
('AltınKG/USD','AltınKG/USD'),
('AltınKG/EUR','AltınKG/EUR'),
('EUR/USD','EUR/USD'),
('USD/TL','USD/TL'),
('EUR/TL','EUR/TL'),
('Gümüş/TL','Gümüş/TL'),
('AUD/TL','AUD/TL'),
('CAD/TL','CAD/TL'),
('GBP/TL','GBP/TL'),
('NOK/TL','NOK/TL'),
('CHF/TL','CHF/TL'),
('DKK/TL','DKK/TL'),
('YEN/TL','YEN/TL'),
('SAR/TL','SAR/TL'),
('SEK/TL','SEK/TL'),
('Yeni Çeyrek','Yeni Çeyrek'),
('Yeni Yarım','Yeni Yarım'),
('Yeni Tam','Yeni Tam'),
('Yeni Gremse','Yeni Gremse'),
('Ziynet 5`li','Ziynet 5`li'),
('Eski Çeyrek','Eski Çeyrek'),
('Eski Yarım','Eski Yarım'),
('Eski Gremse','Eski Gremse'),
('Ata Çeyrek','Ata Çeyrek'),
('Ata Yarım','Ata Yarım'),
('Ata','Ata'),
('Ata 5`li','Ata 5`li'),
('Eski Ata','Eski Ata'),
('Eski Ata 5`li','Eski Ata 5`li'),
('22 Ayar','22 Ayar'),
('18 Ayar','18 Ayar'),
('14 Ayar','14 Ayar'),
]

def SavingChoices():
    choices=Choices.objects.values_list('name1','name2')
    choices=list(itertools.chain(*choices))
    print(choices)
    return(choices)








        