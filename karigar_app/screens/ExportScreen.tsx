import React, { useState } from 'react';
import {
  View, Text, StyleSheet, TouchableOpacity,
  ScrollView, ActivityIndicator, Linking, Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, RADIUS, SHADOW } from '../constants/theme';
import { API_BASE, ENDPOINTS } from '../constants/api';

export default function ExportScreen() {
  const [gemLoading, setGemLoading]   = useState(false);
  const [ondcLoading, setOndcLoading] = useState(false);

  const exportGem = async () => {
    setGemLoading(true);
    try {
      const url = `${API_BASE}${ENDPOINTS.exportGem}`;
      await Linking.openURL(url);
    } catch {
      Alert.alert('Error', 'Could not open export. Check your connection.');
    } finally {
      setGemLoading(false);
    }
  };

  const exportOndc = async () => {
    setOndcLoading(true);
    try {
      const url = `${API_BASE}${ENDPOINTS.exportOndc}`;
      await Linking.openURL(url);
    } catch {
      Alert.alert('Error', 'Could not open export. Check your connection.');
    } finally {
      setOndcLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.title}>Export to Marketplace</Text>
        <Text style={styles.subtitle}>बाज़ार में बेचें — GeM & ONDC</Text>
      </View>

      {/* GeM Card */}
      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <View style={[styles.iconBox, { backgroundColor: '#E8F4FD' }]}>
            <Ionicons name="grid" size={28} color="#2980B9" />
          </View>
          <View style={{ flex: 1, marginLeft: 14 }}>
            <Text style={styles.cardTitle}>GeM Marketplace</Text>
            <Text style={styles.cardSub}>Government e-Marketplace</Text>
          </View>
          <View style={styles.govBadge}>
            <Text style={styles.govBadgeText}>GOV</Text>
          </View>
        </View>

        <View style={styles.features}>
          {['27-column bulk upload CSV', 'HSN codes auto-filled', 'Hindi titles included', 'GSTIN + MRP ready'].map(f => (
            <View key={f} style={styles.featureRow}>
              <Ionicons name="checkmark-circle" size={16} color={COLORS.success} />
              <Text style={styles.featureText}>{f}</Text>
            </View>
          ))}
        </View>

        <TouchableOpacity style={styles.exportBtn} onPress={exportGem} disabled={gemLoading} activeOpacity={0.85}>
          <LinearGradient colors={['#2980B9','#1A6A9A']} style={styles.exportGradient} start={{x:0,y:0}} end={{x:1,y:0}}>
            {gemLoading
              ? <ActivityIndicator color={COLORS.white} />
              : <>
                  <Ionicons name="download-outline" size={18} color={COLORS.white} style={{marginRight:8}} />
                  <Text style={styles.exportBtnText}>Download GeM CSV</Text>
                </>}
          </LinearGradient>
        </TouchableOpacity>
      </View>

      {/* ONDC Card */}
      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <View style={[styles.iconBox, { backgroundColor: '#EAFAF1' }]}>
            <Ionicons name="globe" size={28} color="#27AE60" />
          </View>
          <View style={{ flex: 1, marginLeft: 14 }}>
            <Text style={styles.cardTitle}>ONDC Network</Text>
            <Text style={styles.cardSub}>Open Network for Digital Commerce</Text>
          </View>
          <View style={[styles.govBadge, { backgroundColor: '#EAFAF1' }]}>
            <Text style={[styles.govBadgeText, { color: COLORS.success }]}>OPEN</Text>
          </View>
        </View>

        <View style={styles.features}>
          {['Beckn Protocol 2.0 JSON', 'All buyer apps reached', 'Make-in-India tags', 'GST breakup included'].map(f => (
            <View key={f} style={styles.featureRow}>
              <Ionicons name="checkmark-circle" size={16} color={COLORS.success} />
              <Text style={styles.featureText}>{f}</Text>
            </View>
          ))}
        </View>

        <TouchableOpacity style={styles.exportBtn} onPress={exportOndc} disabled={ondcLoading} activeOpacity={0.85}>
          <LinearGradient colors={[COLORS.success,'#1E8449']} style={styles.exportGradient} start={{x:0,y:0}} end={{x:1,y:0}}>
            {ondcLoading
              ? <ActivityIndicator color={COLORS.white} />
              : <>
                  <Ionicons name="cloud-download-outline" size={18} color={COLORS.white} style={{marginRight:8}} />
                  <Text style={styles.exportBtnText}>Download ONDC JSON</Text>
                </>}
          </LinearGradient>
        </TouchableOpacity>
      </View>

      {/* Info note */}
      <View style={styles.infoBox}>
        <Ionicons name="information-circle-outline" size={18} color={COLORS.primary} />
        <Text style={styles.infoText}>
          All products you've saved will be included in the export. Upload the CSV directly to the GeM seller portal.
        </Text>
      </View>

      <View style={{ height: 60 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container:    { flex: 1, backgroundColor: COLORS.screenBg },
  content:      { padding: 20 },
  header:       { marginBottom: 24, marginTop: 12 },
  title:        { fontSize: 26, fontWeight: '900', color: COLORS.text },
  subtitle:     { fontSize: 14, color: COLORS.textMuted, marginTop: 4 },
  card:         { backgroundColor: COLORS.white, borderRadius: RADIUS.lg, padding: 20, marginBottom: 16, ...SHADOW.sm },
  cardHeader:   { flexDirection: 'row', alignItems: 'center', marginBottom: 16 },
  iconBox:      { width: 52, height: 52, borderRadius: 14, alignItems: 'center', justifyContent: 'center' },
  cardTitle:    { fontSize: 17, fontWeight: '800', color: COLORS.text },
  cardSub:      { fontSize: 12, color: COLORS.textMuted, marginTop: 2 },
  govBadge:     { backgroundColor: '#EBF5FB', paddingHorizontal: 10, paddingVertical: 4, borderRadius: RADIUS.full },
  govBadgeText: { fontSize: 11, fontWeight: '800', color: '#2980B9', letterSpacing: 1 },
  features:     { marginBottom: 16 },
  featureRow:   { flexDirection: 'row', alignItems: 'center', marginBottom: 8 },
  featureText:  { fontSize: 13, color: COLORS.textLight, marginLeft: 8 },
  exportBtn:    { borderRadius: RADIUS.full, overflow: 'hidden' },
  exportGradient: { paddingVertical: 14, flexDirection: 'row', alignItems: 'center', justifyContent: 'center' },
  exportBtnText:{ fontSize: 15, fontWeight: '700', color: COLORS.white },
  infoBox:      { flexDirection: 'row', backgroundColor: '#FFF3EE', borderRadius: RADIUS.md, padding: 14, gap: 10 },
  infoText:     { flex: 1, fontSize: 12, color: COLORS.textLight, lineHeight: 18 },
});
