import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  TextInput, Image, ActivityIndicator, Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, RADIUS, SHADOW } from '../constants/theme';
import { useAppStore } from '../store/useAppStore';
import { calculatePrice, createProduct } from '../services/api';

export default function ReviewScreen({ navigation }: any) {
  const {
    currentCatalog, enhancedImageUrl, selectedLanguage, addProduct,
  } = useAppStore();

  const [materialCost, setMaterialCost] = useState('');
  const [laborHours, setLaborHours]     = useState('');
  const [pricing, setPricing]           = useState<any>(null);
  const [loading, setLoading]           = useState(false);
  const [saving, setSaving]             = useState(false);

  if (!currentCatalog) {
    return (
      <View style={styles.empty}>
        <Ionicons name="alert-circle-outline" size={48} color={COLORS.textMuted} />
        <Text style={styles.emptyText}>No catalog yet. Go back and record first.</Text>
      </View>
    );
  }

  const lang = selectedLanguage.code;
  const displayTitle = lang === 'hi'
    ? currentCatalog.title_hi ?? currentCatalog.title
    : lang === 'en'
    ? currentCatalog.title
    : currentCatalog.title_localized ?? currentCatalog.title;

  const displayDesc = lang === 'hi'
    ? currentCatalog.description_hi ?? currentCatalog.description
    : lang === 'en'
    ? currentCatalog.description
    : currentCatalog.description_localized ?? currentCatalog.description;

  const getPrice = async () => {
    if (!materialCost || !laborHours) {
      Alert.alert('Please enter', 'Material cost and labour hours are required.');
      return;
    }
    setLoading(true);
    try {
      const result = await calculatePrice(
        parseFloat(materialCost),
        parseFloat(laborHours),
        currentCatalog.category,
        currentCatalog.title,
        enhancedImageUrl ?? undefined,
      );
      setPricing(result);
    } catch (e) {
      Alert.alert('Error', 'Could not calculate price. Try again.');
    } finally {
      setLoading(false);
    }
  };

  const saveProduct = async () => {
    if (!pricing) { Alert.alert('Get price first'); return; }
    setSaving(true);
    try {
      const product = await createProduct({
        ...currentCatalog,
        material_cost: parseFloat(materialCost),
        labor_hours: parseFloat(laborHours),
        image_url: enhancedImageUrl,
      });
      addProduct(product);
      Alert.alert('Saved! 🎉', 'Your product is saved.', [
        { text: 'View Products', onPress: () => navigation.navigate('Products') },
        { text: 'Export to GeM/ONDC', onPress: () => navigation.navigate('Export') },
      ]);
    } catch (e) {
      Alert.alert('Error', 'Could not save product.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <View style={styles.header}>
        <Text style={styles.stepTag}>STEP 2 OF 2 — दूसरा कदम</Text>
        <Text style={styles.title}>Review & Price</Text>
      </View>

      {/* Enhanced image */}
      {enhancedImageUrl && (
        <View style={styles.card}>
          <Text style={styles.cardLabel}>📷 Enhanced Photo — साफ़ तस्वीर</Text>
          <Image source={{ uri: enhancedImageUrl }} style={styles.productImage} resizeMode="contain" />
          <View style={styles.chip}>
            <Ionicons name="checkmark-circle" size={14} color={COLORS.success} />
            <Text style={styles.chipText}>Background removed · White canvas</Text>
          </View>
        </View>
      )}

      {/* Generated catalog */}
      <View style={styles.card}>
        <Text style={styles.cardLabel}>📝 AI-Generated Listing</Text>

        <Text style={styles.fieldLabel}>Title (English)</Text>
        <Text style={styles.fieldValue}>{currentCatalog.title}</Text>

        {currentCatalog.title_hi && (
          <>
            <Text style={styles.fieldLabel}>शीर्षक (Hindi)</Text>
            <Text style={styles.fieldValue}>{currentCatalog.title_hi}</Text>
          </>
        )}

        <Text style={styles.fieldLabel}>Description</Text>
        <Text style={styles.fieldValueSmall}>{currentCatalog.description}</Text>

        <View style={styles.tagsRow}>
          <View style={styles.tag}><Text style={styles.tagText}>{currentCatalog.category}</Text></View>
          <View style={styles.tag}><Text style={styles.tagText}>{currentCatalog.craft_technique}</Text></View>
        </View>
      </View>

      {/* Pricing inputs */}
      <View style={styles.card}>
        <Text style={styles.cardLabel}>💰 Smart Pricing — सही दाम</Text>

        <View style={styles.inputRow}>
          <View style={{ flex: 1, marginRight: 8 }}>
            <Text style={styles.inputLabel}>Material Cost (₹)</Text>
            <TextInput
              style={styles.input}
              value={materialCost}
              onChangeText={setMaterialCost}
              keyboardType="numeric"
              placeholder="e.g. 200"
            />
          </View>
          <View style={{ flex: 1 }}>
            <Text style={styles.inputLabel}>Labour Hours</Text>
            <TextInput
              style={styles.input}
              value={laborHours}
              onChangeText={setLaborHours}
              keyboardType="numeric"
              placeholder="e.g. 4"
            />
          </View>
        </View>

        <TouchableOpacity style={styles.priceBtn} onPress={getPrice} disabled={loading}>
          {loading
            ? <ActivityIndicator color={COLORS.white} />
            : <Text style={styles.priceBtnText}>Calculate Price — दाम लगाएं</Text>}
        </TouchableOpacity>

        {pricing && (
          <View style={styles.priceResult}>
            <View style={styles.priceRow}>
              <Text style={styles.priceLabel}>Base Cost</Text>
              <Text style={styles.priceVal}>₹{pricing.base_cost}</Text>
            </View>
            <View style={[styles.priceRow, styles.highlightRow]}>
              <Text style={styles.suggestedLabel}>Suggested Price</Text>
              <Text style={styles.suggestedVal}>₹{pricing.suggested_price}</Text>
            </View>
            <View style={styles.confidenceRow}>
              <Ionicons name="analytics-outline" size={14} color={COLORS.success} />
              <Text style={styles.confidenceText}>Confidence: {pricing.confidence_band}</Text>
            </View>
          </View>
        )}
      </View>

      {/* Save */}
      <TouchableOpacity style={styles.saveBtn} onPress={saveProduct} disabled={saving} activeOpacity={0.85}>
        <LinearGradient
          colors={[COLORS.primary, COLORS.primaryDark]}
          style={styles.saveGradient}
          start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
        >
          {saving
            ? <ActivityIndicator color={COLORS.white} />
            : <>
                <Ionicons name="cloud-upload-outline" size={20} color={COLORS.white} style={{ marginRight: 8 }} />
                <Text style={styles.saveText}>Save Product — सहेजें</Text>
              </>}
        </LinearGradient>
      </TouchableOpacity>

      <View style={{ height: 60 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container:     { flex: 1, backgroundColor: COLORS.screenBg, padding: 16 },
  empty:         { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 40 },
  emptyText:     { fontSize: 14, color: COLORS.textMuted, textAlign: 'center', marginTop: 12 },
  header:        { marginBottom: 20, marginTop: 12 },
  stepTag:       { fontSize: 11, color: COLORS.primary, fontWeight: '700', letterSpacing: 1.5 },
  title:         { fontSize: 26, fontWeight: '900', color: COLORS.text, marginTop: 4 },
  card:          { backgroundColor: COLORS.white, borderRadius: RADIUS.lg, padding: 18, marginBottom: 14, ...SHADOW.sm },
  cardLabel:     { fontSize: 14, fontWeight: '700', color: COLORS.text, marginBottom: 12 },
  productImage:  { width: '100%', height: 220, borderRadius: RADIUS.md, backgroundColor: '#f5f5f5', marginBottom: 10 },
  chip:          { flexDirection: 'row', alignItems: 'center', backgroundColor: '#EAFAF1', padding: 8, borderRadius: RADIUS.md },
  chipText:      { fontSize: 12, color: COLORS.success, marginLeft: 6 },
  fieldLabel:    { fontSize: 11, color: COLORS.textMuted, fontWeight: '600', letterSpacing: 1, marginTop: 10 },
  fieldValue:    { fontSize: 16, fontWeight: '700', color: COLORS.text, marginTop: 2 },
  fieldValueSmall: { fontSize: 13, color: COLORS.textLight, marginTop: 2, lineHeight: 20 },
  tagsRow:       { flexDirection: 'row', gap: 8, marginTop: 12 },
  tag:           { backgroundColor: '#FFF3EE', paddingHorizontal: 12, paddingVertical: 6, borderRadius: RADIUS.full },
  tagText:       { fontSize: 12, color: COLORS.primary, fontWeight: '600' },
  inputRow:      { flexDirection: 'row', marginBottom: 14 },
  inputLabel:    { fontSize: 12, color: COLORS.textMuted, marginBottom: 4 },
  input:         { borderWidth: 1, borderColor: COLORS.border, borderRadius: RADIUS.md, padding: 12, fontSize: 15, backgroundColor: COLORS.screenBg },
  priceBtn:      { backgroundColor: COLORS.primary, borderRadius: RADIUS.md, padding: 14, alignItems: 'center' },
  priceBtnText:  { color: COLORS.white, fontWeight: '700', fontSize: 14 },
  priceResult:   { marginTop: 14, backgroundColor: COLORS.screenBg, borderRadius: RADIUS.md, padding: 14 },
  priceRow:      { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  priceLabel:    { fontSize: 13, color: COLORS.textMuted },
  priceVal:      { fontSize: 13, fontWeight: '600', color: COLORS.text },
  highlightRow:  { backgroundColor: '#FFF3EE', padding: 10, borderRadius: RADIUS.md },
  suggestedLabel:{ fontSize: 15, fontWeight: '700', color: COLORS.text },
  suggestedVal:  { fontSize: 18, fontWeight: '900', color: COLORS.primary },
  confidenceRow: { flexDirection: 'row', alignItems: 'center', marginTop: 8 },
  confidenceText:{ fontSize: 12, color: COLORS.success, marginLeft: 4 },
  saveBtn:       { borderRadius: RADIUS.full, overflow: 'hidden', marginTop: 4 },
  saveGradient:  { paddingVertical: 18, flexDirection: 'row', alignItems: 'center', justifyContent: 'center' },
  saveText:      { fontSize: 16, fontWeight: '700', color: COLORS.white },
});
