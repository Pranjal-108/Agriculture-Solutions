from flask import Flask,render_template,request
from package import prediction
import os
import smtplib
from datetime import datetime

app=Flask(__name__)

crop_name=['Banana','Bajra', 'Barley', 'Bean', 'Black pepper', 'Blackgram', 'Bottle Gourd', 'Brinjal', 'Cabbage', 'Cardamom', 'Carrot', 
'Castor seed', 'Cauliflower', 'Chillies', 'Colocosia', 'Coriander', 'Cotton', 'Cowpea', 'Drum Stick', 'Garlic', 'Guar seed', 'Ginger', 
'Gram', 'Grapes', 'Groundnut', 'Horse-gram', 'Jowar', 'Jute', 'Khesari', 'Lady Finger', 'Lemon', 'Lentil', 'Linseed', 'Maize', 'Mesta', 
'Moong(Green Gram)', 'Moth', 'Onion', 'Orange', 'Papaya', 'Peas & beans (Pulses)', 'Potato', 'Raddish', 'Ragi', 'Rice', 'Safflower', 
'Sannhamp', 'Sesamum', 'Soyabean', 'Sugarcane', 'Sunflower', 'Sweet potato', 'Tapioca', 'Tomato', 'Turmeric', 'Urad', 'Varagu', 'Wheat']

crop_name_hindi=['केला','बाजरा', 'जौ', 'बीन', 'काली मिर्च', 'ब्लैकग्राम', 'बॉटल लौकी', 'बैगन', 'पत्तागोभी', 'इलायची', 'गाजर','कैस्टर सीड्स', 'फूलगोभी',
'मिर्च', 'कोलोसोशिया', 'धनिया', 'कॉटन', 'काउपिया', 'ड्रम स्टिक','लहसुन', 'गौर बीज', 'अदरक', 'ग्राम', 'अंगूर', 'मूंगफली', 'घोड़ा-चना', 'ज्वार', 'जूट', 
'खेसारी','लेडी फिंगर', 'लेमन', 'लेंटिल', 'अलसी', 'मक्का', 'मैस्टा', 'मूंग (ग्रीन ग्राम)', 'मॉथ', 'प्याज', 'ऑरेंज', 'पपीता', 'मटर एंड बीन्स (दालें)', 'आलू', 
'मूली', 'रागी', 'चावल', 'कुसुम','सनहम्प', 'सीसम', 'सोयाबीन', 'गन्ना', 'सूरजमुखी', 'स्वीट पोटैटो', 'टैपिओका', 'टमाटर', 'हल्दी', 'उड़द', 'वरुग', 'व्हीट']

crop_name_hindi_english=['kela','baajara', 'jau', 'been', 'kaalee mirch', 'blaikagraam', 'botal laukee', 'baigan', 'pattaagobhee', 
'ilaayachee', 'gaajar','kaistar seeds', 'phoolagobhee', 'mirch', 'kolososhiya', 'dhaniya', 'kotan', 'kaupiya', 'dram stik','lahasun', 
'gaur beej', 'adarak', 'graam', 'angoor', 'moongaphalee', 'ghoda-chana', 'jvaar', 'joot', 'khesaaree','ledee phingar', 'leman', 'lentil', 
'alasee', 'makka', 'maista', 'moong (green graam)', 'moth', 'pyaaj', 'orenj', 'papeeta', 'matar end beens (daalen)', 'aaloo', 'moolee', 
'raagee', 'chaaval', 'kusum', 'sanahamp', 'seesam', 'soyaabeen', 'ganna', 'soorajamukhee', 'sveet potaito', 'taipioka', 'tamaatar', 'haldee', 
'udad', 'varug', 'vheet']

crop_name_scientific=['Musa','Pennisetum glaucum','Hordeum vulgare','Phaseolus','Piper nigrum','Vigna mungo','Lagenaria siceraria','Solanum melongena','Brassica oleracea var. capitata','Elettaria cardamomum','Daucus carota subsp. sativus',
'Ricinus communis','Brassica oleracea var. botrytis','Capsicum frutescens','Colocasia esculenta','Coriandrum sativum','Gossypium','Vigna unguiculata','Moringa oleifera',
'Allium sativum','Cyamopsis tetragonoloba','Zingiber officinale','Cicer arietinum','Vitis','Arachis hypogaea','Macrotyloma uniflorum','Sorghum','Corchorus capsularis','Lathyrus sativus',
'Abelmoschus esculentus','Citrus × limon','Lens culinaris','Linum usitatissimum','Zea mays','','Vigna radiata','Lepidoptera','Allium cepa','Citrus X sinensis','Carica papaya',
'Pisum sativum','Solanum tuberosum','Raphanus sativus','Eleusine coracana','Oryza sativa','Carthamus tinctorius',
'Crotalaria juncea','Sesamum indicum','Glycine max','Saccharum officinarum','Helianthus','Ipomoea batatas','Manihot esculenta','Solanum lycopersicum','Curcuma longa','Vigna mungo','Paspalum scrobiculatum','Triticum']
'''
print(len(crop_name))
print(len(crop_name_hindi))
print(len(crop_name_hindi_english))
print(len(crop_name_scientific))
'''
@app.route('/')
def index():
    return render_template('prediction.html')

@app.route('/chatbot')
def chat():
    return render_template('chatbot.html')

@app.route('/predict',methods = ['GET','POST'])
def predicted():
    number=1
    crop_img_loc=[]
    crop_detail={}
    new_crop_name=[]
    new_crop_name_hindi=[]
    new_crop_name_hindi_english=[]
    new_crop_name_scientific=[]
    new_number=[]
    area=str(request.form.get('city'))
    #print(area)
    final_output=prediction.predicted(area)
    #final_output=prediction.predict()
    print(final_output)
    print(len(final_output))
    
    '''
    print(crop_name)
    print(crop_name_hindi)
    print(crop_name_hindi_english)
    print(crop_name_scientific)
    print(number)
    '''
    img_loc=os.listdir('./static')
    #print(img_loc)
    for i in final_output:
        for j in img_loc:
            if i+'.jpg'==j:
                crop_img_loc.append(j)
            else:
                pass
    #print(crop_img_loc)

    for i in final_output:
        for j in img_loc:
            for k in crop_name:
                if i+'.jpg'==j and i==k:
                    index=crop_name.index(k)
                    '''
                    print(crop_name.index(k))
                    print(k)
                    print(index)
                    print(i)
                    print(crop_name[index])
                    print(index)
                    print(crop_name[index])
                    '''
                    new_number.append(number)
                    new_crop_name.append(crop_name[index])
                    new_crop_name_hindi.append(crop_name_hindi[index])
                    new_crop_name_hindi_english.append(crop_name_hindi_english[index])
                    new_crop_name_scientific.append(crop_name_scientific[index])
                    number+=1

    
    print(len(new_crop_name))
    print(new_crop_name)
    '''
    print(new_crop_name_hindi)
    print(new_crop_name_hindi_english)
    print(new_crop_name_scientific)
    print(new_number)
    '''
    crop_detail= {a: {b: {c:{d:{e:f}}}} for a,b,c,d,e,f in zip(new_number,new_crop_name,new_crop_name_scientific,crop_img_loc,new_crop_name_hindi,new_crop_name_hindi_english)}
    crop_detail['current_date']=datetime.now().date()

    print(crop_detail)


    return render_template('prediction.html', predict=crop_detail)

@app.route('/test')
def test():
    ab=['a','b','c']
    bc=[1,2,3]
    cd=[4,5,6]
    da=[7,8,9]

    res = [{a: {b:{c:d}}} for (a, b, c,d) in zip(ab,bc,cd,da)]

    print(res)

    dct = {a: {b: {c:d}} for a,b,c,d in zip(ab,bc,cd,da)}
    dct['date']=datetime.now().date()

    for i in dct:
        if i!='date':
            print(i)
            print(dct[i])
            for j in dct[i]:
                print(dct[i][j])
                for k in dct[i][j]:
                    print(dct[i][j][k])
        else:
        # not iterable
            print(i, 'is not iterable')

        return render_template('test.html',result=dct)

@app.route('/send',methods=['GET','POST'])
def email():
    fname=request.form.get('f_name')
    lname=request.form.get('l_name')
    mob=request.form.get('mob')
    email=request.form.get('email')
    msg=request.form.get('msg')
    message=fname+" "+lname+" \nPersonal detail :- "+email+" "+mob+" \nMessage :- "+msg
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login("smartagricultre@gmail.com","Sm@rt123456789")
    server.sendmail("smartagricultre@gmail.com","smartagricultre@gmail.com",message)
    server.quit()
    print("email send")
    resp="Mail sended !!"
    return render_template("index.html",resp_msg=resp)

if __name__ == "__main__":
    app.run(debug=True)
