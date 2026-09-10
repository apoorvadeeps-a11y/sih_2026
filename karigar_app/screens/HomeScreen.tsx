import React, { useEffect } from 'react';
import {
  View, Text, StyleSheet, TouchableOpacity,
  FlatList, ScrollView, StatusBar,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, RADIUS, SHADOW } from '../constants/theme';
import { useAppStore } from '../store/useAppStore';
import { listProducts } from '../services/api';

const GRID = [
  { id: 'new',      icon: 'add-circle-outline',  label: 'New Listing',    labelHi: 'नया सामान',  screen: 'Record',   color: COLORS.primary },
  { id: 'products', icon: 'grid-outline',         label: 'My Products',   labelHi: 'मेरी चीज़ें', screen: 'Products', color: '#3498DB' },
  { id: 'buyers',   icon: 'people-outline',       label: 'Buyers',        labelHi: 'ग्राहक',      screen: 'Export',   color: '#27AE60' },
  { id: 'earnings', icon: 'cash-outline',         label: 'Earnings',      labelHi: 'कमाई (₹)',   screen: 'Products', color: '#8E44AD' },
];

export default function HomeScreen({ navigation }: any) {
  const { selectedLanguage, products, setProducts } = useAppStore();

  useEffect(() => {
    listProducts()
      .then((r) => setProducts(r.products))
      .catch(() => {});
  }, []);

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor={COLORS.screenBg} />

      {/* Top bar */}
      <LinearGradient colors={['#1E1E1E', '#2A2A2A']} style={styles.topBar}>
        <View>
          <Text style={styles.welcome}>WELCOME — नमस्ते 🙏</Text>
          <Text style={styles.userName}>नमस्ते, कारीगर!</Text>
        </View>
        <TouchableOpacity style={styles.micBtn}>
          <Ionicons name="mic" size={22} color={COLORS.white} />
        </TouchableOpacity>
      </LinearGradient>

      <ScrollView style={styles.body} showsVerticalScrollIndicator={false}>

        {/* Voice help banner */}
        <TouchableOpacity
          style={styles.voiceBanner}
          onPress={() => navigation.navigate('Record')}
          activeOpacity={0.85}
        >
          <Ionicons name="mic-circle" size={36} color={COLORS.primary} />
          <View style={{ marginLeft: 12 }}>
            <Text style={styles.voiceBannerTitle}>VOICE HELP — बोलें</Text>
            <Text style={styles.voiceBannerSub}>Speak to sell or get help...</Text>
          </View>
          <Ionicons name="chevron-forward" size={20} color={COLORS.textMuted} style={{ marginLeft: 'auto' }} />
        </TouchableOpacity>

        {/* Verified badge */}
        <View style={styles.badge}>
          <Ionicons name="checkmark-circle" size={16} color={COLORS.success} />
          <Text style={styles.badgeText}>Verified Artisan Partner — प्रमाणित कारीगर</Text>
        </View>

        {/* Grid */}
        <View style={styles.grid}>
          {GRID.map((item) => (
            <TouchableOpacity
              key={item.id}
              style={styles.gridCard}
              onPress={() => navigation.navigate(item.screen)}
              activeOpacity={0.7}
            >
              <View style={[styles.gridIcon, { backgroundColor: item.color + '20' }]}>
                <Ionicons name={item.icon as any} size={28} color={item.color} />
              </View>
              <Text style={styles.gridLabel}>{item.label}</Text>
              <Text style={styles.gridLabelHi}>{item.labelHi}</Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Recent products */}
        {products.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Recent Products — हाल के उत्पाद</Text>
            {products.slice(0, 3).map((p) => (
              <TouchableOpacity
                key={p.id}
                style={styles.productRow}
                onPress={() => navigation.navigate('ProductDetail', { product: p })}
              >
                <View style={styles.productIcon}>
                  <Ionicons name="cube-outline" size={24} color={COLORS.primary} />
                </View>
                <View style={{ flex: 1 }}>
                  <Text style={styles.productTitle} numberOfLines={1}>{p.title}</Text>
                  <Text style={styles.productMeta}>{p.category} · ₹{p.suggested_price}</Text>
                </View>
                <Ionicons name="chevron-forward" size={16} color={COLORS.textMuted} />
              </TouchableOpacity>
            ))}
          </View>
        )}

        <View style={{ height: 100 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container:       { flex: 1, backgroundColor: COLORS.screenBg },
  topBar:          { paddingTop: 52, paddingBottom: 20, paddingHorizontal: 20, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  welcome:         { fontSize: 11, color: '#aaa', letterSpacing: 1.5 },
  userName:        { fontSize: 22, fontWeight: '800', color: COLORS.white, marginTop: 2 },
  micBtn:          { width: 44, height: 44, borderRadius: 22, backgroundColor: COLORS.primary, alignItems: 'center', justifyContent: 'center' },
  body:            { flex: 1 },
  voiceBanner:     { margin: 16, padding: 16, backgroundColor: COLORS.white, borderRadius: RADIUS.lg, flexDirection: 'row', alignItems: 'center', borderLeftWidth: 4, borderLeftColor: COLORS.primary, ...SHADOW.sm },
  voiceBannerTitle:{ fontSize: 13, fontWeight: '700', color: COLORS.text },
  voiceBannerSub:  { fontSize: 13, color: COLORS.textMuted, marginTop: 2 },
  badge:           { flexDirection: 'row', alignItems: 'center', marginHorizontal: 16, marginBottom: 16 },
  badgeText:       { fontSize: 12, color: COLORS.success, marginLeft: 6, fontWeight: '600' },
  grid:            { flexDirection: 'row', flexWrap: 'wrap', paddingHorizontal: 12 },
  gridCard:        { width: '46%', margin: '2%', backgroundColor: COLORS.white, borderRadius: RADIUS.lg, padding: 18, alignItems: 'center', ...SHADOW.sm },
  gridIcon:        { width: 56, height: 56, borderRadius: 28, alignItems: 'center', justifyContent: 'center', marginBottom: 10 },
  gridLabel:       { fontSize: 14, fontWeight: '700', color: COLORS.text },
  gridLabelHi:     { fontSize: 13, color: COLORS.textMuted, marginTop: 2 },
  section:         { margin: 16 },
  sectionTitle:    { fontSize: 14, fontWeight: '700', color: COLORS.text, marginBottom: 12 },
  productRow:      { flexDirection: 'row', alignItems: 'center', backgroundColor: COLORS.white, borderRadius: RADIUS.md, padding: 14, marginBottom: 8, ...SHADOW.sm },
  productIcon:     { width: 40, height: 40, borderRadius: 20, backgroundColor: '#FFF3EE', alignItems: 'center', justifyContent: 'center', marginRight: 12 },
  productTitle:    { fontSize: 14, fontWeight: '600', color: COLORS.text },
  productMeta:     { fontSize: 12, color: COLORS.textMuted, marginTop: 2 },
});
