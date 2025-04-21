import streamlit as st
import numpy as np


st.title("Calcul ta rentabilité by Georges👋")
st.markdown("Ceci est un outil pour t’aider à calculer les dépenses et la rentabilité de ton achat immobilier.")

col1, col2 = st.columns(2)
with col1:
    prix_appt    = st.number_input("Prix appartement", value=200000, step=10000)
    frais_agence = st.number_input("Frais d'agence (opt.)", value=0, step=1000)
    frais_banc   = st.number_input("Frais bancaires/dossiers", value=0, step=1000)
    apport       = st.number_input("Apport perso", value=0, step=1000)
with col2:
    frais_notaire  = st.number_input("Frais notaire", value=0, step=1000)
    travaux        = st.number_input("Travaux (inclus prêt)", value=0, step=1000)
    frais_courtier = st.number_input("Frais courtier", value=0, step=1000)

# montant total du prêt
total_pret = prix_appt + frais_agence + frais_banc + frais_notaire + frais_courtier + travaux
st.write(f"#### 💰 Montant total du prêt: {total_pret:,.2f}€ 💰")

taux_pret = st.number_input("Taux du prêt bancaire (%)", value=4.65, step=0.01) / 100
taux_ass  = st.number_input("Taux assurance prêt (%)", value=0.22, step=0.01) / 100
duree_annees = st.number_input("Durée du prêt (années)", value=25, step=1)
duree_mois   = int(duree_annees * 12)

# PMT manuelle
def pmt(rate, nper, pv):
    if rate == 0:
        return pv / nper
    return (pv * rate * (1 + rate)**nper) / ((1 + rate)**nper - 1)

mens_princ_interet = pmt(taux_pret/12, duree_mois, total_pret)
mens_assurance     = total_pret * taux_ass / 12
mens_with_ass      = mens_princ_interet + mens_assurance

st.write(f"#### 💸 Mensualité sans assurance: {mens_princ_interet:,.2f}€")
st.write(f"#### 🛡️ Mensualité avec assurance: {mens_with_ass:,.2f}€")


# Loyer et charges de co-propriété
loyer          = st.number_input("Loyer (par mois), si mise en location", value=0, step=50)
charges_copro  = st.number_input("Charge de copropriété (annuel)", value=1000, step=100)
charge_copro_mens = charges_copro / 12
st.write(f"Charges de copropriété mensuelles: {charge_copro_mens:,.2f} €")

# Taxe foncière
taxe_foncieres = st.number_input("Taxe foncière (annuelle)", value=1200, step=100)
taxe_foncieres_mens   = taxe_foncieres / 12
st.write(f"Taxe foncière (mensuelle): {charge_copro_mens:,.2f} €")

# Total dépense mensuelles
depenses_mens = mens_with_ass + charge_copro_mens + taxe_foncieres_mens
st.write(f"### 🏦 Dépenses / mois")  
st.write(f"mensualités prêt + charges copro + taxes foncière")
st.write(f"### 💰 {depenses_mens:,.2f}€ 💰")

if loyer > 0:
    cashflow = loyer - (mens_with_ass + taxe_foncieres_mens)
    st.write("Cashflow = loyer - (mensualités du prêt avec assurance + taxes foncières)")
    st.write(f"#### 💵 Cashflow mensuel: {cashflow:,.2f}€")

    if apport > 0 and cashflow is not None:
        rentab = (cashflow / apport) * 100
        st.write(f"#### 📈 Rentabilité: {rentab:,.2f}%")
        st.write("*(Rentabilité cashflow = Cashflow mensuel ÷ Apport perso x100)*")
        st.write("_Les charges de copropriété sont exclues du cashflow (récupérables auprès du locataire)._")

st.write("## Bon Achat ✅!")