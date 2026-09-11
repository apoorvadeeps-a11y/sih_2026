import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput, Image } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../constants/theme';
import { useAppStore } from '../store/useAppStore';

const sampleImages = [
  'https://images.unsplash.com/photo-1517705008128-361805f42e86?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1493106641515-6b5631de4bb9?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=900&q=80',
];

export default function ReviewScreen({ navigation }: any) {
  const { currentCatalog, currentImageUri, setCurrentCatalog, addProduct } = useAppStore();
  const [productName, setProductName] = useState(currentCatalog?.title_hi ?? 'मिट्टी का बर्तन');
  const [description, setDescription] = useState(currentCatalog?.description_hi ?? 'मिट्टी से बनी पारंपरिक कढ़ाई कलाकृति...');
  const [category, setCategory] = useState(currentCatalog?.category ?? 'मिट्टी के Crafted Pottery');

  const saveAndNext = () => {
    const nextCatalog = {
      ...(currentCatalog ?? {}),
      title: productName,
      title_hi: productName,
      description: description,
      description_hi: description,
      category,
      craft_technique: currentCatalog?.craft_technique ?? 'Terracotta',
      source_language: currentCatalog?.source_language ?? 'hi',
    };

    setCurrentCatalog(nextCatalog);
    addProduct({
      id: `product-${Date.now()}`,
      sku: 'KAR-' + Math.floor(Math.random() * 900 + 100),
      title: productName,
      title_hi: productName,
      description,
      description_hi: description,
      category,
      craft_technique: 'Terracotta',
      material_cost: 180,
      labor_hours: 3,
      base_cost: 540,
      suggested_price: 950,
      confidence_band: 'High',
      source_language: 'hi',
      image_url: currentImageUri ?? sampleImages[0],
      created_at: new Date().toISOString(),
    });

    navigation.navigate('Products');
  };

  return (
    <View style={styles.container}>
      <View style={styles.topBar}>
        <Text style={styles.time}>9:41</Text>
        <View style={styles.statusIcons}>
          <Ionicons name="cellular" size={14} color="#1A1A1A" />
          <Ionicons name="wifi" size={14} color="#1A1A1A" />
          <Ionicons name="battery-full" size={16} color="#1A1A1A" />
        </View>
      </View>

      <View style={styles.headerRow}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons name="chevron-back" size={22} color="#1A1A1A" />
        </TouchableOpacity>
        <Text style={styles.pageTitle}>Review Details • विचार जाँच</Text>
        <Ionicons name="flash" size={22} color="#1A1A1A" />
      </View>

      <View style={styles.content}>
        <View style={styles.photoRow}>
          {(currentImageUri ? [currentImageUri] : sampleImages).map((uri, index) => (
            <Image key={`${uri}-${index}`} source={{ uri }} style={styles.thumb} resizeMode="cover" />
          ))}
        </View>

        <View style={styles.verifyBox}>
          <Ionicons name="checkmark-circle" size={18} color={COLORS.success} />
          <Text style={styles.verifyText}>AI identified: Terracotta Pottery • मिट्टी के बर्तन</Text>
        </View>

        <TouchableOpacity style={styles.aiBox}>
          <Ionicons name="mic-circle" size={26} color={COLORS.primary} />
          <Text style={styles.aiText}>Speak to edit or describe your product</Text>
        </TouchableOpacity>

        <View style={styles.fieldBlock}>
          <View style={styles.fieldLabelRow}>
            <Text style={styles.fieldLabel}>PRODUCT NAME • सामान</Text>
            <Ionicons name="create-outline" size={16} color="#4B4B4B" />
          </View>
          <TextInput value={productName} onChangeText={setProductName} style={styles.fieldInput} />
        </View>

        <View style={styles.fieldBlock}>
          <View style={styles.fieldLabelRow}>
            <Text style={styles.fieldLabel}>DESCRIPTION • विवरण</Text>
            <Ionicons name="create-outline" size={16} color="#4B4B4B" />
          </View>
          <TextInput value={description} onChangeText={setDescription} multiline style={[styles.fieldInput, styles.multiLine]} />
        </View>

        <View style={styles.fieldBlock}>
          <View style={styles.fieldLabelRow}>
            <Text style={styles.fieldLabel}>CATEGORY • श्रेणी</Text>
            <Ionicons name="create-outline" size={16} color="#4B4B4B" />
          </View>
          <TextInput value={category} onChangeText={setCategory} style={styles.fieldInput} />
        </View>

        <TouchableOpacity style={styles.primaryBtn} onPress={saveAndNext}>
          <Text style={styles.primaryBtnText}>Next: Set Price • मूल्य निर्धारित करें →</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F5F2EE', alignItems: 'center' },
  topBar: { width: '100%', paddingTop: 10, paddingHorizontal: 16, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  time: { fontSize: 16, fontWeight: '700', color: '#1A1A1A' },
  statusIcons: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  headerRow: { width: '100%', paddingHorizontal: 18, paddingTop: 16, paddingBottom: 10, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  pageTitle: { fontSize: 18, fontWeight: '700', color: '#181818' },
  content: { width: '100%', paddingHorizontal: 18, paddingTop: 8, paddingBottom: 20 },
  photoRow: { flexDirection: 'row', gap: 8, marginBottom: 12 },
  thumb: { width: 78, height: 84, borderRadius: 12, borderWidth: 1, borderColor: '#DAD2CD' },
  verifyBox: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#EFFAF2', borderRadius: 12, borderWidth: 1, borderColor: '#A9DABE', paddingHorizontal: 12, paddingVertical: 10, marginBottom: 12 },
  verifyText: { marginLeft: 8, color: '#2D7A4F', fontSize: 12.5, fontWeight: '600', flexShrink: 1 },
  aiBox: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#FFF5F1', borderWidth: 1.5, borderColor: '#E7A183', borderRadius: 14, paddingHorizontal: 12, paddingVertical: 12, marginBottom: 12 },
  aiText: { marginLeft: 10, fontSize: 13, color: '#D66236', flexShrink: 1 },
  fieldBlock: { backgroundColor: '#FBFAF9', borderWidth: 1, borderColor: '#E9E2DD', borderRadius: 14, paddingHorizontal: 14, paddingTop: 12, paddingBottom: 8, marginBottom: 12 },
  fieldLabelRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 },
  fieldLabel: { fontSize: 12, fontWeight: '700', color: '#5E5E5E', letterSpacing: 0.6 },
  fieldInput: { fontSize: 15, color: '#222222', fontWeight: '600', minHeight: 24, paddingVertical: 0 },
  multiLine: { minHeight: 60, textAlignVertical: 'top' },
  primaryBtn: { marginTop: 10, backgroundColor: '#E76D2B', borderRadius: 14, paddingVertical: 14, alignItems: 'center', justifyContent: 'center' },
  primaryBtnText: { color: '#FFFFFF', fontWeight: '700', fontSize: 14 },
});
