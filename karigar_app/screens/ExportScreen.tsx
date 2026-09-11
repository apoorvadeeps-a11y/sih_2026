import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS, SHADOW } from '../constants/theme';

const buyers = [
  { name: 'राजेश ऑर्गेनिक फैब', location: 'नई दिल्ली', rating: '4.8', detail: 'हाथ से बने टेराकोटा कुकर के सेट, मिट्टी के बर्तन और पारंपरिक भारतीय दीये' },
  { name: 'दिल्ली हाट क्राफ्ट्स कंपनी', location: 'जयपुर, राजस्थान', rating: '4.9', detail: 'प्रीमियम लोकल होम डेकोर, हाथ से नक़्काशी किए गुलदस्ते और देसी सजावटी टेराकोटा कलाकृतियां' },
];

export default function ExportScreen({ navigation }: any) {
  const [selectedCategory, setSelectedCategory] = useState('मिट्टी के बर्तन');

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.topRow}>
          <TouchableOpacity onPress={() => navigation.navigate('Home')}><Ionicons name="chevron-back" size={24} color={COLORS.text} /></TouchableOpacity>
          <Text style={styles.title}>Find Buyers • ग्राहक खोजें</Text>
          <View style={styles.roundIcon}><Ionicons name="mic" size={18} color={COLORS.text} /></View>
        </View>
        <Text style={styles.subtitle}>अपने पास के शौक व्यापारियों और हस्तशिल्प निवेदकों को खोजें</Text>
        <View style={styles.searchBox}><Ionicons name="search" size={20} color="#818181" /><Text style={styles.searchText}>Search buyers or cities...</Text><Ionicons name="mic" size={18} color={COLORS.primary} /></View>
        <Text style={styles.sectionLabel}>DEMAND CATEGORIES • मांग की श्रेणियां</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.chips}>
          {['मिट्टी के बर्तन', 'हस्तकला वस्त्र', 'पीतल की कला'].map((category) => (
            <TouchableOpacity key={category} style={[styles.chip, selectedCategory === category && styles.chipActive]} onPress={() => setSelectedCategory(category)}>
              <Text style={[styles.chipText, selectedCategory === category && styles.chipTextActive]}>{category}</Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
        <View style={styles.locationBanner}><Ionicons name="location-outline" size={18} color={COLORS.success} /><Text style={styles.locationText}>जयपुर के पास (5 किमी के अंदर) 3 सक्रिय खरीदार मिले</Text></View>
        {buyers.map((buyer) => (
          <View key={buyer.name} style={styles.buyerCard}>
            <View style={styles.buyerHeader}><View style={styles.avatar}><Ionicons name="person" size={24} color="#AF7660" /></View><View style={styles.buyerIdentity}><Text style={styles.buyerName}>{buyer.name}</Text><Text style={styles.buyerLocation}>📍 {buyer.location}</Text></View><View style={styles.rating}><Text style={styles.ratingText}>★ {buyer.rating}</Text></View></View>
            <Text style={styles.buyingLabel}>CURRENTLY BUYING • मांग</Text>
            <Text style={styles.buyerDetail}>{buyer.detail}</Text>
            <TouchableOpacity style={styles.connectButton} onPress={() => Alert.alert('Connect request sent', `We will connect you with ${buyer.name}.`)}><Ionicons name="call-outline" size={16} color={COLORS.white} /><Text style={styles.connectText}>Connect • संपर्क करें</Text></TouchableOpacity>
          </View>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F5F2EE' },
  content: { paddingHorizontal: 16, paddingTop: 18, paddingBottom: 30 },
  topRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  title: { fontSize: 19, fontWeight: '800', color: COLORS.text },
  subtitle: { fontSize: 12, color: COLORS.textMuted, marginTop: 14, marginBottom: 14 },
  roundIcon: { width: 38, height: 38, borderRadius: 19, backgroundColor: '#F2EDE7', alignItems: 'center', justifyContent: 'center' },
  searchBox: { height: 46, backgroundColor: COLORS.white, borderWidth: 1.5, borderColor: '#E8DDD5', borderRadius: 14, paddingHorizontal: 12, flexDirection: 'row', alignItems: 'center', gap: 9 },
  searchText: { flex: 1, color: '#858585', fontSize: 14 },
  sectionLabel: { fontSize: 10, fontWeight: '800', color: '#727272', marginTop: 14, marginBottom: 8 },
  chips: { gap: 8 },
  chip: { paddingHorizontal: 12, paddingVertical: 8, borderRadius: 16, backgroundColor: COLORS.white, borderWidth: 1, borderColor: '#E8E0DB' },
  chipActive: { backgroundColor: COLORS.primary, borderColor: COLORS.primary },
  chipText: { fontSize: 12, color: COLORS.text, fontWeight: '700' },
  chipTextActive: { color: COLORS.white },
  locationBanner: { marginTop: 12, paddingHorizontal: 12, paddingVertical: 10, borderRadius: 10, backgroundColor: '#EDF5EB', flexDirection: 'row', alignItems: 'center', gap: 7 },
  locationText: { fontSize: 11, color: '#4D7951', fontWeight: '700' },
  buyerCard: { backgroundColor: COLORS.white, borderRadius: 16, borderWidth: 1, borderColor: '#EEE5DF', padding: 12, marginTop: 14, ...SHADOW.sm },
  buyerHeader: { flexDirection: 'row', alignItems: 'center' },
  avatar: { width: 40, height: 40, borderRadius: 20, backgroundColor: '#F2E6DC', alignItems: 'center', justifyContent: 'center' },
  buyerIdentity: { flex: 1, marginLeft: 10 },
  buyerName: { fontSize: 14, fontWeight: '800', color: COLORS.text },
  buyerLocation: { fontSize: 11, color: COLORS.textMuted, marginTop: 2 },
  rating: { backgroundColor: '#FFF8EA', borderRadius: 12, paddingHorizontal: 8, paddingVertical: 5 },
  ratingText: { fontSize: 11, color: '#A17A32', fontWeight: '800' },
  buyingLabel: { fontSize: 9, fontWeight: '800', color: '#828282', marginTop: 12 },
  buyerDetail: { fontSize: 12, lineHeight: 17, color: COLORS.textLight, marginTop: 4 },
  connectButton: { height: 40, backgroundColor: '#6877A7', borderRadius: 20, marginTop: 12, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 7 },
  connectText: { color: COLORS.white, fontSize: 13, fontWeight: '800' },
});
