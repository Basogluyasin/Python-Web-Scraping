import requests
from bs4 import BeautifulSoup
import pandas as pd


class Mnk:
    def __init__(self,site_url="https://www.mnkhome.com/"):
        self.site_url = site_url
        self.linkler = []
        self.hazir_urun = []
        
        
        
    #Url yapısı
    def get_url(self):
        return f"{self.site_url}{self.kategori}"
    
    
    
    #Url oluşturma, istek atma, parse
    def get_request(self):
        url = self.get_url()
        html = requests.get(url)
        self.soup = BeautifulSoup(html.content,"html.parser")
        
        
                
    #Kategorideki her bir ürünün html kodu
    def urunler_url(self):
        self.get_request()
        
        urun_link = self.soup.find_all("div", {"itemscope":"itemscope"})
        for i in urun_link:
            urun_url = i.find("span",{"itemprop":"url"}).get("content")
            url = self.site_url+urun_url
            self.linkler.append(url)
        
        return self.linkler
    
            
    #Sırasıyla her ürünün url'si, istek atma ve parse
    def urun_bilgileri(self):
        self.urunler_url()
        self.urun_sayisi = len(self.linkler)
        
        sayac = 1
        for link in self.linkler:
            
            html = requests.get(link)
            self.soup1= BeautifulSoup(html.content,"html.parser")
            
            
            #Ürün Adı
            self.urun_adi = self.soup1.find("h1",{"class":"fl col-12 text-regular m-top m-bottom"}).text
            
            
            #Ürün Kodu
            kod1 = self.soup1.find("div",{"class":"fl col-12 text-code pt"}).strong.text
            self.kod ="DCW"+kod1
            
            
            #Ürün Stok
            self.stok = self.soup1.find("div",{"id":"productInfo"}).find_all("div")[2].strong.text
            
            
            #Ürün Fiyatı
            self.fiyat = round(float(self.soup1.find("span",attrs={"itemprop":"price"}).get("content")),2)
            
            
            #Ürün Açıklama
            self.ürünÖzellikleri = list()
            self.ürünEbatları = list()
            
            
            #Ürün özellikleri boş olan ürünler için except
            try:
                self.özellikler = self.soup1.find("div",{"id":"productDetailTab"}).div.ul.find_all("li")
                
                
                for özellik in self.özellikler:
                    self.ürün_özellik = özellik.text
                    self.ürünÖzellikleri.append(self.ürün_özellik)
                
                
            except:
                continue
        
            
        
            #Ürün ebatları boş veya farklı html etiketinde olan ürünler için except
            try:
                self.ebatlar = self.soup1.find("div",{"id":"productDetailTab"}).div.div.ul.find_all("li")
            
                for ebat in self.ebatlar:
                    self.ürün_ebat = ebat.text
                    self.ürünEbatları.append(self.ürün_ebat)
            
            except:
                self.ebatlar = self.soup1.find("div",{"id":"productDetailTab"}).div.ul.ul.find_all("li")
            
                for ebat in self.ebatlar:
                    self.ürün_ebat = ebat.text
                    self.ürünEbatları.append(self.ürün_ebat)
           
        
            
            self.urun = {
                    "Ürün Adı": self.urun_adi,
                    "Ürün Kodu": self.kod,
                    "Stok": self.stok,
                    "Fiyat": self.fiyat,
                    "Açıklama": "Ürün Özellikleri: " + " ".join(self.ürünÖzellikleri) + "Ürün Ebatları: " +  ",".join(self.ürünEbatları)
                }
            
            
            
            #Ürün Fotoğrafları
            self.foto = self.soup1.find("ul",{"id":"productImage"}).find_all("li")
            
            n=0
            for i in self.foto:
                a = i.find("a").get("href")
                fotolar = {"foto"+str(n):a}
                n+=1
                
                
                self.urun.update(fotolar)
            
            
            self.hazir_urun.append(self.urun)
        
        
            print(f" Tamamlanan: {sayac}/{self.urun_sayisi}")
            sayac+=1
    
    
    
    #Pandas ile dataframe'e çevirme ve csv olarak kaydetme
    def dataFrame(self):
        self.urun_bilgileri()
        
        
        df = pd.DataFrame(self.hazir_urun)
        
        df.to_csv(self.dosya_ismi+".csv", index = False, sep=";")
    
    
                      
    #Scraping
    def scraping(self):
        self.kategori = input("Kategorinin link uzantısını gir: ")
        self.dosya_ismi = input("Dosya adını gir: ")
        
        self.dataFrame()