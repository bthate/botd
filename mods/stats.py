# BOTLIB - Framework to program bots.
#
# mods/stats.py (suicide stats)

import bot
import datetime
import lo
import lo.clk
import lo.tms
import random
import time


def init(kernel):
    for name in wanted.keys():
        obj = wanted.get(name, None)
        if obj:
            e = lo.hdl.Event()
            e.txt = ""
            e.rest = name
            for key in obj.keys():
                val = obj.get(key, None)
                if val:
                    sec = seconds(val)
                    repeater = lo.clk.Repeater(sec, stat, e, name="stats.%s" % key)
                    repeater.start()

year_formats = [
    "%b %H:%M",
    "%b %H:%M:%S",
    "%a %H:%M %Y",
    "%a %H:%M",
    "%a %H:%M:%S",
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d-%m",
    "%m-%d",
    "%Y-%m-%d %H:%M:%S",
    "%d-%m-%Y %H:%M:%S",
    "%d-%m %H:%M:%S",
    "%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%d-%m-%Y %H:%M",
    "%d-%m %H:%M",
    "%m-%d %H:%M",
    "%H:%M:%S",
    "%H:%M"
]


class ENOSTATS(Exception):

    pass

def day():
    return str(datetime.datetime.today()).split()[0]

def get_time(daystr):
    for f in year_formats:
        try:
            t = time.mktime(time.strptime(daystr, f))
            return t
        except Exception:
            pass

def today():
    return datetime.datetime.today().timestamp()

def to_day(daystring):
    line = ""
    daystr = str(daystring)
    for word in daystr.split():
        if "-" in word:
            line += word + " "
        elif ":" in word:
            line += word
    if "-" not in line:
        line = day() + " " + line
    try:
        return get_time(line.strip())
    except ValueError:
        pass

startdate = "2018-10-05 00:00:00"
#startdate = "2012-09-13 00:00:00"
starttime = to_day(startdate)
source = "https://bitbucket.org/botd/botlib"

def seconds(nr, period="jaar"):
    if not nr:
        return nr
    return nrsec.get(period) / float(nr)

def nr(name):
    for key in wanted.keys():
        obj = wanted.get(key, None)
        for n in obj.keys():
            if n == name:
                return obj.get(n)
    raise ENOSTATS(name)

def stats(event, **kwargs):
    args = event.args
    txt = "Sinds %s\n" % time.ctime(starttime)
    delta = time.time() - starttime
    k = bot.get_kernel()
    for name, obj in wanted.items():
        for key, val in obj.items():
            try:
                needed = seconds(nr(key))
            except ENOSTATS:
                return
            name = key
            nrtimes = int(delta/needed)
            txt = "%s #%s" % (name.upper(), nrtimes)
            if name in omschrijving:
                txt += " (%s)" % omschrijving.get(name)
            txt += " elke %s" % lo.tms.elapsed(seconds(nr(name)))
            if name in urls:
                txt += " - %s" % urls.get(name)
            if name in tags:
                txt += " %s" % tags.get(name)
            else:
                 txt += " %s" % random.choice(list(tags.values()))
            k.fleet.announce(txt)

def stat(event, **kwargs):
    name = event.rest or "suicide" 
    if "." in name:
        name = name.split(".")[-1]
    name = name.lower()
    delta = time.time() - starttime
    awake = time.time() - today()
    try:
        needed = seconds(nr(name))
    except ENOSTATS:
        return
    k = bot.get_kernel()
    if needed:
        nrtimes = int(delta/needed)
        txt = "%s #%s" % (name.upper(), nrtimes)
        if name in omschrijving:
            txt += " (%s)" % omschrijving.get(name)
        txt += " elke %s" % lo.tms.elapsed(seconds(nr(name)))
        if name in urls:
            txt += " - %s" % urls.get(name)
        if name in tags:
            txt += " %s" % tags.get(name)
        else:
            txt += " %s" % random.choice(list(tags.values()))
        k.fleet.announce(txt)

oorzaak = lo.Object()
oorzaak.suicide = 1800
oorzaak.psychosestoornis = 12000

nrsec = lo.Object()
nrsec.dag = 24 * 60 * 60.0
nrsec.jaar = 365 * nrsec.dag
nrsec.weekend = 2 / 7 * (24 * 60 * 60.0 * 365) / 52
nrsec.avond = 16 / 24 * (24 * 60 * 60.0)

times = lo.Object()
times.weekend = 2 / 7 * (24 * 60 * 60.0 * 365) / 52
times.avond = 16 / 24 * (24 * 60 * 60.0)
times.dag = 24 * 60 * 60.0
times.jaar = 365 * 24 * 60 * 60.0

# PER JAAR

rechter = lo.Object()
rechter.ibs = 8861
rechter.rm = 17746
rechter.vwm = 6657
rechter.mvv = 4431
rechter.vm = 6690
rechter.mev = 65
rechter.zm= 3

suicidejaar = lo.Object()
suicidejaar.y2008 = 1435
suicidejaar.y2009 = 1525
suicidejaar.y2010 = 1600
suicidejaar.y2011 = 1647
suicidejaar.y2012 = 1753
suicidejaar.y2013 = 1857
suicidejaar.y2014 = 1839
suicidejaar.y2015 = 1871 
suicidejaar.y2016 = 1894
suicidejaar.y2017 = 1917

ziekenhuis = lo.Object()
ziekenhuis.y2010 = 7800
ziekenhuis.y2011 = 9600
ziekenhuis.y2012 = 9200
ziekenhuis.y2013 = 8300
ziekenhuis.y2014 = 8500

seh = lo.Object()
seh.y2010 = 13700
seh.y2011 = 16000
seh.y2012 = 15800
seh.y2013 = 13300
seh.y2014 = 14000

e33 = lo.Object()
e33.melding = 61000

cijfers = lo.Object()
cijfers.melding = 61000
cijfers.opnames = 24338
cijfers.crisis = 150000
cijfers.oordeel = 150000
cijfers.pogingen = 94000
cijfers.incidenten = 66000
cijfers.poh = 1300000
cijfers.vergiftigingen = 25262
cijfers.overlast = 18000
cijfers.insluiting = 240000
cijfers.aangiftes = 134000
cijfers.suicide = 1871
cijfers.burenoverlast = 12000
cijfers.uitzetting = 5900
cijfers.volwassendoop = 500
cijfers.tumor = 12000
cijfers.detox = 65654
cijfers.acuut = 8000
cijfers.spoedeisendpoging = 14000
cijfers.weguitkliniek = 2539
cijfers.bewindvoering = 295000
cijfers.suicidegedachtes = 410000
cijfers.psychosestoornis = 13076
cijfers.oorzaak = cijfers.psychosestoornis + cijfers.suicide

oordeel = lo.Object()
oordeel.verwijs = cijfers.crisis * 0.85 
oordeel.uitstroom = cijfers.crisis * 0.05
oordeel.opname = cijfers.crisis * 0.10

alarm = lo.Object()
alarm.politie = 0.30 * cijfers.crisis
alarm.hap = 0.40 * cijfers.crisis
alarm.keten = 0.30 * cijfers.crisis

suicide = lo.Object()
suicide.suicide = suicidejaar.y2017

pogingen = lo.Object()
pogingen.pogingen = cijfers.pogingen

poging = lo.Object()
poging.ziekenhuis = ziekenhuis.y2014
poging.seh = seh.y2014

# PER BEVOLKING

drugs = lo.Object()
drugs.speed = 20000
drugs.cocaine = 50000
drugs.alcohol = 400000
drugs.wiet = 500000

medicijnen = lo.Object()
medicijnen.amitriptyline = 189137
medicijnen.paroxetine = 186028
medicijnen.citalopram = 154620
medicijnen.oxazepam = 133608
medicijnen.venlafaxine = 112000
medicijnen.mirtazapine = 110742
medicijnen.quetiapine = 84414
medicijnen.diazepam = 72000
medicijnen.sertraline = 68000
medicijnen.haloperidol = 59825

dbc = lo.Object()
dbc.middelgebondenstoornissen = 33060
dbc.somatoformestoornissen = 21841
dbc.cognitievestoornissen = 25717
dbc.angststoornissen = 54458
dbc.aanpassingsstoornissen = 43079
dbc.depressievestoornissen = 102361
dbc.eetstoornissen = 8688
dbc.restgroepdiagnose = 16996
dbc.ontbrekendeprimairediagnose = 3030
dbc.andereproblemenredenvoorzorg = 49286
dbc.schizofrenieenanderepsychotischestoornissen = 6798
dbc.bipolairestoornissen = 3569
dbc.posttraumatischestressstoornis = 24716
dbc.persoonlijkheidsstoornissen = 36574
dbc.adhd = 25951
dbc.gedrag = 1176
dbc.kindertijdoverig = 1035
dbc.autismespectrum = 9436

# PER DAG

halfwaarde = lo.Object()
halfwaarde.zyprexa = 30
halfwaarde.abilify = 75
halfwaarde.haldol = 30
halfwaarde.alprazolam = 11
halfwaarde.orap = 55
halfwaarde.paracetamol = 2.5
halfwaarde.lorazepam = 12
halfwaarde.paroxetine = 21 
halfwaarde.citalopram = 35
halfwaarde.oxazepam = 8.2
halfwaarde.quetiapine = 6
halfwaarde.diazepam = 100
halfwaarde.wiet = 7

perdag = lo.Object()
perdag.medicijnen = medicijnen
perdag.drugs = drugs

# DISPLAY

tags = lo.Object()
tags.keten = "#burgemeester"
tags.politie = "#broodjepindakaas"
tags.hap = "#triagetrien"
tags.verwijs = "#maandagweer"
tags.uitstroom = "#zorgwekkend"
tags.opname = "#meermedicijn"  
tags.crisis = "#triade"
tags.suicide = "#wetverplichteggz"
tags.pogingen = "#prettigweekend" 
tags.incidenten = "#jammerdan"    
tags.acuut = "#geenbedvoorjou"    
tags.zorgmijder = "#helaas"       
tags.inwoners = "#gebodenvrucht"  
tags.crisis = "#medicijnen"
tags.alarm = "#telaat"
tags.oordeel = "#geencrisis"
tags.vergiftigingen = "#overduur"
tags.neurotoxisch = "#overdosis" 
tags.schizofrenie = "#gifmedicijn"
tags.angst = "#gifmedicijn"
tags.depressie = "#gifmedicijn"
tags.meds = "#gifmedicijn"
tags.ibs = "#overlast"
tags.rm = "#benadeling"
tags.vwm = "#maatregel"
tags.vm = "#nogeven"
tags.mvv = "#direct!!"
tags.mev = "#kieserzelfvoor"
tags.om = "#ffkijken#"
tags.zm = "#zelfwat?"

omschrijving = lo.Object()
omschrijving.ibs = "inbewaringstelling"
omschrijving.rm = "rechterlijke machtiging"
omschrijving.vm = "voorlopige rechterlijke machtiging"
omschrijving.mvv = "machtiging voortgezet verblijf"
omschrijving.vwm = "voorwaardelijke rechterlijke machtiging"
omschrijving.mev = "machtiging eigen verzoek"
omschrijving.zm = "zelfbinding machtiging"
omschrijving.om = "observatie machtiging"
omschrijving.keten = "ggz besluit tot crisisbeoordeling"
omschrijving.politie = "politie vraagt om crisisbeoordeling"
omschrijving.hap = 'huisartsenpost vraagt om crisisbeoordeeling'
omschrijving.verwijs = "crisisdienst maakt vervolg afspraak"
omschrijving.uitstroom = "crisisdienst maakt geen vervolgafspraak"
omschrijving.opname = 'niet meten, maar off-label tot "therapeutische" werking'
omschrijving.suicide = "behandelplan is niet op te vragen"
omschrijving.pogingen = "suicide poging is mislukt"
omschrijving.weekend = "niet bereikbaar tot maandag"
omschrijving.avond = "wachten tot de volgende ochtend"
omschrijving.incidenten = "code 33 gemeld bij politie - overlast veroorzaakt door gestoord/overspannen persoon"
omschrijving.acuut = "spoedeisende psychiatrische hulp ingeschakeld"
omschrijving.zorgmijder = "patient durft geen zorg meer te ontvangen"
omschrijving.inwoners = "5% van de nederlanders heeft GGZ problemen"
omschrijving.crisis = "situatie is dusdanig dat men vraagt om een crisisbeoordeling"
omschrijving.alarm = "opschaling van zorg NA de crisis"
omschrijving.oordeel = "brengt patient aan voor beoordeling"
omschrijving.vergiftigingen = "opgestapelde werking van giftige medicijnen"
omschrijving.neurotoxisch = "2 maanden zyprexa is genoeg"
omschrijving.speed = "speed gebruikt"
omschrijving.cocaine = "cocaine gebruikt"
omschrijving.alcohol = "alcohol gedronken"
omschrijving.wiet = "wietje gerookt"
omschrijving.antipsychotica = "antipsychotica ingenomen"
omschrijving.antidepresiva = "antidepressiva ingenomen"
omschrijving.slaapmiddel = "slaapmiddel ingenomen"
omschrijving.ambulant = "patient/behandelaar contact"
omschrijving.verslaving = "diagnose verslaving"
omschrijving.schizofrenie = "diagnose schizofrenie"
omschrijving.depressie = "depressieve patient"
omschrijving.amitriptyline = "depressie"
omschrijving.paroxetine = "antipsychotica"
omschrijving.citalopram = "sedatie"
omschrijving.oxazepam = "sedatie"
omschrijving.venlafaxine = "depressie"
omschrijving.mirtazapine = "depressie"
omschrijving.quetiapine = "antipschotica"
omschrijving.diazepam = "sedatie"
omschrijving.sertraline = "depressie"
omschrijving.haloperidol = "antipsyochotica"
omschrijving.verslaafden = "diagnose verslaving"
omschrijving.inwoners = "koningrijk der nederlanden"
omschrijving.arbeidshandicap = "volledig afgekeurd"
omschrijving.huisartsen = "praktijkhouder in nederland"
omschrijving.opnames = "opgenomen in ziekenhuis"
omschrijving.zorgmijder = "zorgontwijker"
omschrijving.middelgebondenstoornissen = "drugverslaving"
omschrijving.somatoformestoornissen = "lichamelijke klachten heeft waarvoor geen somatische oorzaak (lichamelijke ziekte) gevonden is"
omschrijving.cognitievestoornissen = "waarnemingsvermogen is verstoord"
omschrijving.angststoornissen = "fobien en sociaal niet meer kunnen functioneren"
omschrijving.aanpassingsstoornissen = "karakterstoornis, men is al te gevormd"
omschrijving.depressievestoornissen = "somberheid troef"
omschrijving.eetstoornissen = "vreetkicks, bolimia, anorexia"
omschrijving.restgroepdiagnose = "niet anders vernoemd, valt niet in een standaard diagnose"
omschrijving.ontbrekendeprimairediagnose = "geen duidelijke diagnose te stellen"
omschrijving.andereproblemenredenvoorzorg = "niet in standaard zorg te plaatsen"
omschrijving.schizofrenieenanderepsychotischestoornissen = "stemmen horen, waan denkbeelden"
omschrijving.bipolairestoornissen = "stemmingswisselingen"
omschrijving.posttraumatischestressstoornis = "stress na trauma"
omschrijving.persoonlijkheidsstoornissen = "aanpassings problemen"
omschrijving.adhd = "te druk, te veel energie"
omschrijving.gedrag = "moelijk opvoedbaar"
omschrijving.kindertijdoverig = "vroegtijdig trauma"
omschrijving.autismespectrum = "valt in een autisme categorie"
omschrijving.seh = "spoedeisende hulp"
omschrijving.psychosestoornis = "een door de psychose zelf overleden persoon"
omschrijving.oorzaak = "oorzaak van overlijden"

urls = lo.Object()
urls.ibs = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.rm = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.vm = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.mvv = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.vw = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.mev = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.zb = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.ob = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.zm = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.iatrogeen = "https://www.nrc.nl/nieuws/2011/04/22/eenvijfde-van-de-opnames-te-wijten-aan-medicijnen-12012115-a426225"
urls.opname = "http://www.tijdschriftvoorpsychiatrie.nl/issues/434/articles/8318"
urls.crisis = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html"
urls.tuchtrecht = "http://tuchtrecht.overheid.nl/zoeken/resultaat/uitspraak/2014/ECLI_NL_TGZRAMS_2014_94?zaaknummer=2013%2F221&Pagina=1&ItemIndex=1"
urls.suicide = "http://www.cbs.nl/nl-NL/menu/themas/bevolking/publicaties/artikelen/archief/2014/2014-4204-wm.htm"
urls.incident = "https://www.wodc.nl/onderzoeksdatabase/2337-de-effectiviteit-van-de-politiele-taakuitvoering-en-de-taken-en-verantwoordelijkheden-van-andere-partijen.aspx"
urls.zorgmijder = "http://www.gezondheidsraad.nl/sites/default/files/samenvatting_noodgedwongen_0.pdf"
urls.acuut = "http://www.gezondheidsraad.nl/sites/default/files/samenvatting_noodgedwongen_0.pdf"
urls.wvggz = "https://www.dwangindezorg.nl/de-toekomst/wetsvoorstellen/wet-verplichte-geestelijke-gezondheidszorg"
urls.politie = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html"
urls.hap = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html"
urls.keten = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html"
urls.verwijs = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html"
urls.uitstroom = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html" 
urls.opnames = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html"
urls.vergifitigingen = "http://www.umcutrecht.nl/getmedia/f9f152e2-8638-4ffc-a05f-fce72f5f416a/NVIC-Jaaroverzicht-2014.pdf.aspx?ext=.pdf"
urls.neurotoxisch = "http://www.umcutrecht.nl/getmedia/f9f152e2-8638-4ffc-a05f-fce72f5f416a/NVIC-Jaaroverzicht-2014.pdf.aspx?ext=.pdf"
urls.incidenten = "http://www.dsp-groep.nl/userfiles/file/Politie%20en%20verwarde%20personen%20_DSP-groep.pdf"
urls.ambulant = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/"
urls.verslaving = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/"
urls.poh = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/"
urls.meds = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/"
urls.depressie = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/"
urls.angst = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/"
urls.schizofrenie = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/"
urls.detox = "https://www.jellinek.nl/vraag-antwoord/hoeveel-mensen-zijn-verslaafd-en-hoeveel-zijn-er-in-behandeling/"
urls.verslaafden = "https://www.jellinek.nl/vraag-antwoord/hoeveel-mensen-zijn-verslaafd-en-hoeveel-zijn-er-in-behandeling/"
urls.volwassendoop = ""
urls.arbeidshandicap = "http://www.nationalezorggids.nl/gehandicaptenzorg/nieuws/27841-ruim-100-000-mensen-op-sociale-werkplaats.html"
urls.overlast = "http://nos.nl/artikel/2075227-verwarde-huurders-veroorzaken-steeds-meer-overlast.html"
urls.insluiting = "http://www.tweedekamer.nl/downloads/document?id=78ee0f32-7487-4bcc-ba01-e01ace2bc4b4&title=Arrestantenzorg%20Nederland%20Landelijke%20rapportage.pdf"
urls.zyprexa = "http://www.ema.europa.eu/docs/nl_NL/document_library/EPAR_-_Product_Information/human/000287/WC500055611.pdf"
urls.factor = "http://nos.nl/artikel/2090676-aantal-incidenten-met-verwarde-mensen-flink-onderschat.html"
urls.dbc = "https://www.nza.nl/1048076/1048181/Marktscan_ggz_2014_deel_B_en_beleidsbrief.pdf"
urls.dbs2015 = "https://www.rijksoverheid.nl/documenten/rapporten/2016/05/25/marktscan-ggz"
urls.medicijnen="https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/geestelijke-gezondheidszorg/row-5/welke-geneesmiddelen-worden-het-meest-voorgeschreven-in-de-ggz/"
urls.pogingen="http://www.nfzp.nl/wp/wp-content/uploads/2010/09/Einddocument-AF0943-Kwaliteitsdcoument-Ketenzorg-bij-Suicidaliteit.pdf"
urls.suicidegedachte="http://www.nfzp.nl/wp/wp-content/uploads/2010/09/Einddocument-AF0943-Kwaliteitsdcoument-Ketenzorg-bij-Suicidaliteit.pdf"
urls.ziekenhuisopnames = "https://www.tweedekamer.nl/kamerstukken/detail?id=2016D13371&did=2016D13371"
urls.seh = "https://www.tweedekamer.nl/kamerstukken/detail?id=2016D13371&did=2016D13371"
urls.epa = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/ernstige-psychiatrische-aandoeningen/"
urls.rechter = "https://www.ggdghorkennisnet.nl/?file=43865&m=1541606110&action=file.download"
urls.psychosestoornis = "https://www.volksgezondheidenzorg.info/echi-indicators/mortality#node-disease-specific-mortality"

soort = lo.Object()
soort.alarm = "patient"
soort.oordeel = "arts"
soort.neurotoxisch = "patient"
soort.angst = "patient"
soort.depressie = "patient"
soort.schizofrenie = "patient"
soort.ibs = "burgemeester"
soort.rm = "civiele rechter"
soort.vm = "civiele rechter"
soort.mvv = "civiele rechter"
soort.vwm = "civiele rechter"
soort.ev = "civiele rechter"
soort.om ="civiele rechter"
soort.zm = "civiele rechter"
soort.politie = "agent"
soort.hap = "huisarts"
soort.keten  = "spv/psychiater"
soort.verwijs = "crisisdienst"
soort.uitstroom = "eigen behandelaar"
soort.suicide = "slachtoffer"
soort.crisis = "burger"
soort.pogingen = "wanhopige patient"
soort.incidenten = "hulproepende patient"
soort.acuut = "vergiftigde patient"
soort.meds = "toegediende patient"
soort.amitriptyline = "patient"
soort.paroxetine = "patient"
soort.citalopram = "patient"
soort.oxazepam = "patient"
soort.venlafaxine = "patient"
soort.mirtazapine = "patient"
soort.quetiapine = "patient"
soort.diazepam = "patient"
soort.sertrali = "patient"
soort.haloperidol = "patient"
soort.insluiting = "politie"
soort.ambulant = "casemanager"
soort.verslaafden = "gebruiker"
soort.slaapmiddel = "insomnia patient"

# WANTED

wanted = lo.Object()
wanted.oorzaak = oorzaak
wanted.pogingen = pogingen

demo = lo.Object()
demo.dbc = dbc
demo.medicijnen = medicijnen
demo.drugs = drugs
