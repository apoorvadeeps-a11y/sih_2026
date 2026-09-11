import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { COLORS } from '../constants/theme';
import { useAppStore } from '../store/useAppStore';

const sampleImages = [
  'https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?auto=format&fit=crop&w=300&q=80',
  'https://images.unsplash.com/photo-1594736797933-d0501ba2fe65?auto=format&fit=crop&w=300&q=80',
  'https://images.unsplash.com/photo-1543854589-fddf0c9c6e32?auto=format&fit=crop&w=300&q=80',
];
const cameraImage = 'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?auto=format&fit=crop&w=1200&q=85';

export default function RecordScreen({ navigation }: any) {
  const { setCurrentImageUri, setCurrentCatalog } = useAppStore();
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  const pickImage = async () => {
    const result = await ImagePicker.launchCameraAsync({ mediaTypes: ImagePicker.MediaTypeOptions.Images, quality: 0.8 });
    if (!result.canceled) {
      const uri = result.assets[0].uri;
      setSelectedImage(uri);
      setCurrentImageUri(uri);
      setCurrentCatalog({ title: 'Clay Pottery Bowl', title_hi: 'मिट्टी का बर्तन', description: 'Handcrafted terracotta pottery bowl made with natural clay and artisan finishing.', description_hi: 'प्राकृतिक मिट्टी से बना हाथ से निर्मित मृद्भांड, सुंदर फिनिश के साथ।', category: 'Home Decor', craft_technique: 'Terracotta', source_language: 'hi' });
      Alert.alert('Image captured', 'Proceed to review your listing.');
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.topBar}><Text style={styles.time}>9:41</Text><View style={styles.statusIcons}><Ionicons name="cellular" size={14} color="#1A1A1A" /><Ionicons name="wifi" size={14} color="#1A1A1A" /><Ionicons name="battery-full" size={16} color="#1A1A1A" /></View></View>
      <View style={styles.headerRow}><TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}><Ionicons name="chevron-back" size={22} color="#555" /></TouchableOpacity><View><Text style={styles.step}>STEP 1 OF 2 • पहला कदम</Text><Text style={styles.title}>Take Photo • फोटो लें</Text></View><TouchableOpacity style={styles.voiceCircle}><Ionicons name="mic" size={18} color="#555" /></TouchableOpacity></View>
      <View style={styles.captureWrap}>
        <Text style={styles.helperText}>Take photo of your product</Text>
        <Text style={styles.helperTextHi}>अपनी बनाई हुई चीज़ की फोटो खींचिए</Text>
        <View style={styles.cameraFrame}><Image source={{ uri: selectedImage ?? cameraImage }} style={styles.image} resizeMode="cover" /><View style={styles.overlayGrid} /><View style={styles.liveBadge}><View style={styles.liveDot} /><Text style={styles.liveText}>LIVE VIEWFINDER</Text></View></View>
        <View style={styles.sampleRow}><Text style={styles.sampleTitle}>SAMPLES</Text><View style={styles.sampleThumbs}>{sampleImages.map((uri) => <Image key={uri} source={{ uri }} style={styles.sampleThumb} resizeMode="cover" />)}</View></View>
        <TouchableOpacity style={styles.voiceButton}><View style={styles.voiceButtonIcon}><Ionicons name="mic" size={24} color={COLORS.white} /></View><View><Text style={styles.voiceLabel}>VOICE HELP • बोलें</Text><Text style={styles.voiceText}>तस्वीर लेने के लिए क्लिक करें</Text></View></TouchableOpacity>
        <View style={styles.bottomActionRow}><TouchableOpacity style={styles.iconButton} onPress={() => navigation.navigate('Products')}><Ionicons name="images-outline" size={24} color="#555" /></TouchableOpacity><TouchableOpacity style={styles.captureButton} onPress={pickImage}><View style={styles.captureInner}><Ionicons name="camera-outline" size={28} color={COLORS.white} /></View></TouchableOpacity><TouchableOpacity style={styles.iconButton} onPress={() => navigation.navigate('Review')}><Ionicons name="flash-outline" size={25} color="#555" /></TouchableOpacity></View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#FDFCFB' }, topBar: { paddingTop: 12, paddingHorizontal: 16, flexDirection: 'row', justifyContent: 'space-between' }, time: { fontSize: 14, fontWeight: '700', color: '#1A1A1A' }, statusIcons: { flexDirection: 'row', gap: 6 },
  headerRow: { paddingHorizontal: 17, paddingTop: 16, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }, backButton: { width: 39, height: 39, borderRadius: 20, backgroundColor: '#F4EFE9', alignItems: 'center', justifyContent: 'center' }, step: { fontSize: 10, color: '#777', fontWeight: '700', textAlign: 'center' }, title: { fontSize: 19, color: COLORS.text, fontWeight: '900', marginTop: 2 }, voiceCircle: { width: 39, height: 39, borderRadius: 20, backgroundColor: '#F4EFE9', alignItems: 'center', justifyContent: 'center' },
  captureWrap: { paddingHorizontal: 17, paddingTop: 22 }, helperText: { fontSize: 13, color: COLORS.text, fontWeight: '700', textAlign: 'center' }, helperTextHi: { fontSize: 17, color: '#555', textAlign: 'center', marginTop: 6, marginBottom: 20 }, cameraFrame: { height: 246, borderRadius: 20, overflow: 'hidden', borderWidth: 3, borderColor: '#D36132', backgroundColor: '#DDD4CF', position: 'relative' }, image: { width: '100%', height: '100%' }, overlayGrid: { position: 'absolute', left: 28, right: 28, top: 20, bottom: 20, borderWidth: 1.5, borderColor: '#FFF', borderStyle: 'dashed', borderRadius: 8, opacity: 0.8 }, liveBadge: { position: 'absolute', left: 12, bottom: 10, paddingHorizontal: 9, paddingVertical: 5, borderRadius: 12, backgroundColor: 'rgba(35,35,35,.75)', flexDirection: 'row', alignItems: 'center', gap: 5 }, liveDot: { width: 7, height: 7, borderRadius: 4, backgroundColor: '#E76D2B' }, liveText: { color: COLORS.white, fontSize: 9, fontWeight: '800' },
  sampleRow: { marginTop: 20, flexDirection: 'row', alignItems: 'center' }, sampleTitle: { fontSize: 10, color: '#777', fontWeight: '800', width: 57 }, sampleThumbs: { flexDirection: 'row', gap: 10 }, sampleThumb: { width: 38, height: 38, borderRadius: 7, borderWidth: 1, borderColor: '#D8D0CA' },
  voiceButton: { marginTop: 18, height: 58, borderRadius: 16, borderWidth: 1, borderColor: '#E6DDD6', backgroundColor: '#FFF', paddingHorizontal: 12, flexDirection: 'row', alignItems: 'center', shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 4, elevation: 1 }, voiceButtonIcon: { width: 40, height: 40, borderRadius: 20, backgroundColor: '#3F865A', alignItems: 'center', justifyContent: 'center', marginRight: 11 }, voiceLabel: { fontSize: 10, color: '#777', fontWeight: '800' }, voiceText: { fontSize: 14, color: COLORS.text, fontWeight: '800', marginTop: 2 },
  bottomActionRow: { marginTop: 17, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }, iconButton: { width: 48, height: 48, borderRadius: 24, backgroundColor: '#F4EFE9', alignItems: 'center', justifyContent: 'center' }, captureButton: { width: 70, height: 70, borderRadius: 35, borderWidth: 3, borderColor: '#D36132', alignItems: 'center', justifyContent: 'center' }, captureInner: { width: 56, height: 56, borderRadius: 28, backgroundColor: '#D36132', alignItems: 'center', justifyContent: 'center' },
});
