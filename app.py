import streamlit as st
import numpy as np


st.title("A Combien revient un achat immobilier ? Georges 👋")
st.markdown("Ceci est un outil t'aide à calculer les dépenses liées à ton achat immobilier.")

st.markdown("-----------------------------------------")
st.subheader("1. Ta capacité d'emprunt")

revenu_mensuel = st.number_input("Ton revenu net mensuel (avant impôts)", value=0, step=100)
if revenu_mensuel > 0:
    capacite_emprunt = revenu_mensuel * 0.35
    st.write(f"👉 Ta capacité d'emprunt **maximale estimée** est de : **{capacite_emprunt:,.2f} €** par mois")
    st.caption("💬 Calcul basé sur la règle des 35% d'endettement maximum")




# --------------------------------------------------------------------------------- 
st.markdown("-----------------------------------------")
st.subheader("2. Le montant total à emprunter")

# Evaluation du montant de prêt
col1, col2 = st.columns(2)
with col1:
    prix_appt    = st.number_input("Prix appartement", value=200000, step=10000)
    mode_agence = st.radio("Frais d'agence en % ou €", ["En €", "En %"], horizontal=True, key="mode_agence")
    if mode_agence == "En %":
        frais_agence_pct = st.number_input("Frais d'agence (%)", value=0, step=1)
        frais_agence = prix_appt * (frais_agence_pct / 100)
    else:
        frais_agence = st.number_input("Frais d'agence (€)", value=0, step=500)
    frais_banc   = st.number_input("Frais bancaires/dossiers", value=0, step=1000)
    apport       = st.number_input("Apport perso", value=0, step=1000)
with col2:
    mode_notaire = st.radio("Frais notaire en % ou €", ["En €", "En %"], horizontal=True, key="mode_notaire")
    if mode_notaire == "En %":
        frais_notaire_pct = st.number_input("Frais de notaire (%)", value=0, step=1)
        frais_notaire = prix_appt * (frais_notaire_pct / 100)
    else:
        frais_notaire = st.number_input("Frais de notaire (€)", value=0, step=500)
    travaux        = st.number_input("Travaux (inclus prêt)", value=0, step=1000)
    frais_courtier = st.number_input("Frais courtier", value=0, step=1000)

# montant total du prêt
total_pret = prix_appt + frais_agence + frais_banc + frais_notaire + frais_courtier + travaux - apport
st.write(f"#### Montant total du prêt")
st.write(f"💰 {total_pret:,.2f}€ 💰")




# ---------------------------------------------------------------------------------
st.markdown("-----------------------------------------")
st.write(f"### 3. Les mensualités du prêt")
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

st.write(f"#### Mensualité sans assurance:")
st.write(f"💰 {mens_princ_interet:,.2f}€ 💰")
st.write(f"#### Mensualité avec assurance:")
st.write(f"💰 {mens_with_ass:,.2f}€ 💰")




# ---------------------------------------------------------------------------------
st.markdown("-----------------------------------------")
st.write(f"### 4. Le coût mensuel (charges incluses)")
# charges de co-propriété et taxes
charges_copro  = st.number_input("Charges de copropriété / an", value=1000, step=100)
charge_copro_mens = charges_copro / 12
st.write(f"Soit {charge_copro_mens:,.2f}€ / mois")

# Taxe foncière
taxe_foncieres = st.number_input("Taxe foncière / an", value=1200, step=100)
taxe_foncieres_mens   = taxe_foncieres / 12
st.write(f"Soit {charge_copro_mens:,.2f}€ / mois")

# Total dépense mensuelles
depenses_mens = mens_with_ass + charge_copro_mens + taxe_foncieres_mens
st.write(f"#### Mensualités prêt + Charges copro + Taxe foncière")
st.write(f"💰 {depenses_mens:,.2f}€ 💰")




# ---------------------------------------------------------------------------------
st.markdown("-----------------------------------------")
st.subheader("5. Si mises en location")
loyer = st.number_input("Loyer (par mois), si mise en location", value=0, step=50)
if loyer > 0:
    cashflow = loyer - (mens_with_ass + taxe_foncieres_mens)
    st.write("Cashflow = loyer - (mensualités du prêt avec assurance + taxes foncières)")
    st.write(f"#### 💵 Cashflow mensuel")
    st.write(f": {cashflow:,.2f}€")

    if apport > 0 and cashflow is not None:
        rentab = (cashflow / apport) * 100
        st.write(f"#### 📈 Rentabilité: {rentab:,.2f}%")
        st.write("*(Rentabilité cashflow = Cashflow mensuel ÷ Apport perso x100)*")
        st.write("_Les charges de copropriété sont exclues du cashflow (récupérables auprès du locataire)._")

st.write("### 🥳🎈 Merci d'avoir étudier tes chiffres!")