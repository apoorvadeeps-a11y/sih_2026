import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, StatusBar } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../constants/theme';
import { useAppStore } from '../store/useAppStore';

const cards = [
  { title: 'New Listing', hindi: 'नया सामान', icon: 'image-outline', action: 'Record', tint: '#F8F2ED' },
  { title: 'My Products', hindi: 'मेरी चीज़ें', icon: 'albums-outline', action: 'Products', tint: '#F8F5F1' },
  { title: 'Buyers', hindi: 'ग्राहक', icon: 'people-outline', action: 'Market', tint: '#FAF7F4' },
  { title: 'Earnings', hindi: 'कमाई (₹)', icon: 'wallet-outline', action: 'Products', tint: '#F2F7F2' },
] as const;

export default function HomeScreen({ navigation }: any) {
  const { selectedLanguage } = useAppStore();

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <View style={styles.phoneFrame}>
        <View style={styles.topBar}><Text style={styles.time}>9:41</Text><View style={styles.statusIcons}><Ionicons name="cellular" size={14} color="#1A1A1A" /><Ionicons name="wifi" size={14} color="#1A1A1A" /><Ionicons name="battery-full" size={16} color="#1A1A1A" /></View></View>
        <View style={styles.welcomeRow}>
          <View style={styles.avatar}><Ionicons name="color-palette" size={20} color="#C46A3D" /></View>
          <View style={styles.welcomeCopy}><Text style={styles.eyebrow}>WELCOME • स्वागत है</Text><Text style={styles.greeting}>नमस्ते, मित्रा!</Text><Text style={styles.language}>{selectedLanguage.native}</Text></View>
          <TouchableOpacity style={styles.voiceCircle} onPress={() => navigation.navigate('Record')}><Ionicons name="mic" size={18} color="#4A4A4A" /></TouchableOpacity>
        </View>
        <TouchableOpacity style={styles.voiceHelp} onPress={() => navigation.navigate('Record')}><View style={styles.voiceHelpIcon}><Ionicons name="mic" size={20} color={COLORS.white} /></View><View><Text style={styles.voiceLabel}>VOICE HELP • बोलें</Text><Text style={styles.voiceTitle}>Speak to sell or get help...</Text></View></TouchableOpacity>
        <View style={styles.cardGrid}>{cards.map((card) => <TouchableOpacity key={card.title} style={[styles.actionCard, { backgroundColor: card.tint }]} onPress={() => navigation.navigate(card.action)}><Ionicons name={card.icon as any} size={42} color="#171717" /><Text style={styles.cardTitle}>{card.title}</Text><Text style={styles.cardHindi}>{card.hindi}</Text></TouchableOpacity>)}</View>
        <View style={styles.spacer} />
        <View style={styles.verified}><Ionicons name="shield-checkmark-outline" size={19} color="#518165" /><Text style={styles.verifiedText}>Verified Artisan Partner • प्रमाणित कारीगर</Text></View>
        <View style={styles.bottomNav}><NavItem icon="home" label="Home" active onPress={() => navigation.navigate('Home')} /><NavItem icon="cube-outline" label="Products" onPress={() => navigation.navigate('Products')} /><NavItem icon="storefront-outline" label="Market" onPress={() => navigation.navigate('Market')} /><NavItem icon="person-outline" label="Profile" onPress={() => navigation.navigate('Language')} /></View>
      </View>
    </View>
  );
}

function NavItem({ icon, label, active, onPress }: { icon: any; label: string; active?: boolean; onPress: () => void }) { return <TouchableOpacity style={styles.navItem} onPress={onPress}><Ionicons name={icon} size={22} color={active ? COLORS.primary : '#555'} /><Text style={[styles.navLabel, active && styles.navLabelActive]}>{label}</Text><Text style={[styles.navHindi, active && styles.navLabelActive]}>{label === 'Home' ? 'गृह' : label === 'Products' ? 'सामान' : label === 'Market' ? 'बाज़ार' : 'प्रोफाइल'}</Text></TouchableOpacity>; }

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#DAD6D1', justifyContent: 'center', alignItems: 'center', paddingVertical: 20 },
  phoneFrame: { width: 390, maxWidth: '100%', height: 844, backgroundColor: '#FDFCFB', borderRadius: 28, overflow: 'hidden', borderWidth: 2, borderColor: '#D9D4D0', shadowColor: '#000', shadowOffset: { width: 0, height: 8 }, shadowOpacity: 0.18, shadowRadius: 18, elevation: 10 },
  topBar: { paddingTop: 12, paddingHorizontal: 16, flexDirection: 'row', justifyContent: 'space-between' },
  time: { fontSize: 14, fontWeight: '700', color: '#1A1A1A' }, statusIcons: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  welcomeRow: { paddingHorizontal: 18, paddingTop: 17, flexDirection: 'row', alignItems: 'center' },
  avatar: { width: 43, height: 43, borderRadius: 22, backgroundColor: '#F1E5D8', alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: '#D68254' },
  welcomeCopy: { flex: 1, marginLeft: 10 }, eyebrow: { fontSize: 10, color: '#777', fontWeight: '700' }, greeting: { fontSize: 18, color: COLORS.text, fontWeight: '900', marginTop: 2 }, language: { display: 'none' },
  voiceCircle: { width: 39, height: 39, borderRadius: 20, backgroundColor: '#F4EFE9', alignItems: 'center', justifyContent: 'center' },
  voiceHelp: { marginHorizontal: 18, marginTop: 28, padding: 11, borderWidth: 1, borderColor: '#E8DDD5', borderRadius: 17, backgroundColor: '#FFF', flexDirection: 'row', alignItems: 'center', shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 4, elevation: 1 },
  voiceHelpIcon: { width: 42, height: 42, borderRadius: 21, backgroundColor: '#D35D2C', alignItems: 'center', justifyContent: 'center', marginRight: 10 },
  voiceLabel: { fontSize: 10, color: '#777', fontWeight: '800' }, voiceTitle: { fontSize: 15, color: COLORS.text, fontWeight: '800', marginTop: 3 },
  cardGrid: { paddingHorizontal: 18, marginTop: 12, flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  actionCard: { width: '48.4%', height: 118, borderRadius: 17, borderWidth: 1, borderColor: '#EEE7E1', padding: 14, justifyContent: 'center' },
  cardTitle: { fontSize: 12, color: COLORS.text, fontWeight: '800', marginTop: 7 }, cardHindi: { fontSize: 16, color: '#555', fontWeight: '700', marginTop: 1 },
  spacer: { flex: 1 }, verified: { height: 50, marginHorizontal: 14, borderWidth: 1, borderColor: '#9ABD9F', backgroundColor: '#F3FAF2', borderRadius: 10, flexDirection: 'row', alignItems: 'center', paddingHorizontal: 12, gap: 8 }, verifiedText: { color: '#568061', fontSize: 12, fontWeight: '700' },
  bottomNav: { height: 73, marginTop: 10, borderTopWidth: 1, borderTopColor: '#ECE7E3', backgroundColor: '#FFF', flexDirection: 'row', justifyContent: 'space-around', paddingTop: 8 }, navItem: { width: 68, alignItems: 'center' }, navLabel: { fontSize: 10, color: '#555', marginTop: 3 }, navHindi: { fontSize: 8, color: '#777', marginTop: 1 }, navLabelActive: { color: COLORS.primary, fontWeight: '800' },
});
