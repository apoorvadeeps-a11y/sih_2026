import React, { useState, useRef } from 'react';
import {
  View, Text, StyleSheet, TouchableOpacity,
  ScrollView, ActivityIndicator, Alert, Image,
} from 'react-native';
import { Audio } from 'expo-av';
import * as ImagePicker from 'expo-image-picker';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, RADIUS, SHADOW } from '../constants/theme';
import { useAppStore } from '../store/useAppStore';
import { voiceToCatalog, enhanceImage } from '../services/api';

type Step = 'idle' | 'recording' | 'processing' | 'done';

export default function RecordScreen({ navigation }: any) {
  const { selectedLanguage, setCurrentCatalog, setCurrentImageUri, setEnhancedImageUrl } = useAppStore();

  const [step, setStep] = useState<Step>('idle');
  const [recordingObj, setRecordingObj] = useState<Audio.Recording | null>(null);
  const [audioUri, setAudioUri] = useState<string | null>(null);
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [statusMsg, setStatusMsg] = useState('');

  // ── Voice recording ───────────────────────────────────────
  const startRecording = async () => {
    try {
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({ allowsRecordingIOS: true, playsInSilentModeIOS: true });
      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY,
      );
      setRecordingObj(recording);
      setStep('recording');
    } catch (e) {
      Alert.alert('Error', 'Could not start recording. Please allow microphone access.');
    }
  };

  const stopRecording = async () => {
    if (!recordingObj) return;
    await recordingObj.stopAndUnloadAsync();
    const uri = recordingObj.getURI();
    setRecordingObj(null);
    setAudioUri(uri ?? null);
    setStep('idle');
  };

  // ── Photo pick ───────────────────────────────────────────
  const pickImage = async () => {
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.8,
    });
    if (!result.canceled) {
      setImageUri(result.assets[0].uri);
      setCurrentImageUri(result.assets[0].uri);
    }
  };

  const pickFromGallery = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.8,
    });
    if (!result.canceled) {
      setImageUri(result.assets[0].uri);
      setCurrentImageUri(result.assets[0].uri);
    }
  };

  // ── Process ───────────────────────────────────────────────
  const processAll = async () => {
    if (!audioUri && !imageUri) {
      Alert.alert('Add input', 'Please record your voice or take a photo first.');
      return;
    }
    setStep('processing');
    try {
      // Process in parallel where possible
      const tasks: Promise<any>[] = [];

      if (audioUri) {
        setStatusMsg('🎙️ Transcribing your voice...');
        tasks.push(voiceToCatalog(audioUri));
      }
      if (imageUri) {
        setStatusMsg('🖼️ Enhancing your photo...');
        tasks.push(enhanceImage(imageUri));
      }

      const results = await Promise.allSettled(tasks);

      let catalog = null;
      let enhancedUrl = null;

      let idx = 0;
      if (audioUri) {
        const r = results[idx++];
        if (r.status === 'fulfilled') catalog = r.value;
      }
      if (imageUri) {
        const r = results[idx++];
        if (r.status === 'fulfilled') enhancedUrl = r.value;
      }

      if (catalog) setCurrentCatalog(catalog);
      if (enhancedUrl) setEnhancedImageUrl(enhancedUrl);

      setStep('done');
      navigation.navigate('Review');
    } catch (e: any) {
      setStep('idle');
      Alert.alert('Error', e?.message ?? 'Something went wrong. Please try again.');
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.stepTag}>STEP 1 OF 2 — पहला कदम</Text>
        <Text style={styles.title}>Record & Capture</Text>
        <Text style={styles.subtitle}>अपनी बनाई हुई चीज़ का फ़ोटो लें</Text>
      </View>

      {/* Voice section */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>🎤  Record Voice Note</Text>
        <Text style={styles.cardSub}>Speak about your product in {selectedLanguage.native}</Text>

        <TouchableOpacity
          style={[styles.recordBtn, step === 'recording' && styles.recordBtnActive]}
          onPress={step === 'recording' ? stopRecording : startRecording}
          activeOpacity={0.8}
        >
          <Ionicons
            name={step === 'recording' ? 'stop-circle' : 'mic-circle'}
            size={64}
            color={step === 'recording' ? COLORS.error : COLORS.primary}
          />
          <Text style={styles.recordBtnText}>
            {step === 'recording' ? 'Tap to Stop Recording' : 'Hold to Record'}
          </Text>
        </TouchableOpacity>

        {audioUri && (
          <View style={styles.doneChip}>
            <Ionicons name="checkmark-circle" size={18} color={COLORS.success} />
            <Text style={styles.doneChipText}>Voice recorded ✓</Text>
          </View>
        )}
      </View>

      {/* Photo section */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>📷  Product Photo</Text>
        <Text style={styles.cardSub}>Any background is fine — AI will clean it</Text>

        {imageUri ? (
          <View>
            <Image source={{ uri: imageUri }} style={styles.preview} resizeMode="cover" />
            <TouchableOpacity style={styles.retakeBtn} onPress={pickImage}>
              <Text style={styles.retakeBtnText}>Retake Photo</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <View style={styles.photoRow}>
            <TouchableOpacity style={styles.photoBtn} onPress={pickImage} activeOpacity={0.8}>
              <Ionicons name="camera" size={32} color={COLORS.primary} />
              <Text style={styles.photoBtnText}>Camera</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.photoBtn} onPress={pickFromGallery} activeOpacity={0.8}>
              <Ionicons name="images" size={32} color={COLORS.primary} />
              <Text style={styles.photoBtnText}>Gallery</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>

      {/* Process button */}
      {step === 'processing' ? (
        <View style={styles.processingBox}>
          <ActivityIndicator size="large" color={COLORS.primary} />
          <Text style={styles.processingText}>{statusMsg}</Text>
          <Text style={styles.processingSubText}>This takes 20–40 seconds...</Text>
        </View>
      ) : (
        <TouchableOpacity style={styles.nextBtn} onPress={processAll} activeOpacity={0.85}>
          <LinearGradient
            colors={[COLORS.primary, COLORS.primaryDark]}
            style={styles.nextGradient}
            start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
          >
            <Ionicons name="sparkles" size={20} color={COLORS.white} style={{ marginRight: 8 }} />
            <Text style={styles.nextText}>Generate Catalog — AI से बनाएं</Text>
          </LinearGradient>
        </TouchableOpacity>
      )}

      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container:     { flex: 1, backgroundColor: COLORS.screenBg },
  content:       { padding: 20 },
  header:        { marginBottom: 24, marginTop: 12 },
  stepTag:       { fontSize: 11, color: COLORS.primary, fontWeight: '700', letterSpacing: 1.5 },
  title:         { fontSize: 26, fontWeight: '900', color: COLORS.text, marginTop: 4 },
  subtitle:      { fontSize: 14, color: COLORS.textMuted, marginTop: 4 },
  card:          { backgroundColor: COLORS.white, borderRadius: RADIUS.lg, padding: 20, marginBottom: 16, ...SHADOW.sm },
  cardTitle:     { fontSize: 16, fontWeight: '700', color: COLORS.text, marginBottom: 4 },
  cardSub:       { fontSize: 13, color: COLORS.textMuted, marginBottom: 16 },
  recordBtn:     { alignItems: 'center', padding: 20, borderRadius: RADIUS.lg, backgroundColor: '#FFF3EE', borderWidth: 2, borderColor: '#F5DDD5', borderStyle: 'dashed' },
  recordBtnActive: { backgroundColor: '#FFEAEA', borderColor: COLORS.error },
  recordBtnText: { fontSize: 14, color: COLORS.text, marginTop: 8, fontWeight: '600' },
  doneChip:      { flexDirection: 'row', alignItems: 'center', marginTop: 12, backgroundColor: '#EAFAF1', padding: 10, borderRadius: RADIUS.md },
  doneChipText:  { color: COLORS.success, fontWeight: '600', marginLeft: 6 },
  preview:       { width: '100%', height: 200, borderRadius: RADIUS.md, marginBottom: 12 },
  retakeBtn:     { alignItems: 'center', padding: 10 },
  retakeBtnText: { color: COLORS.primary, fontWeight: '600' },
  photoRow:      { flexDirection: 'row', gap: 12 },
  photoBtn:      { flex: 1, alignItems: 'center', padding: 24, borderRadius: RADIUS.lg, backgroundColor: '#FFF3EE', borderWidth: 1, borderColor: '#F5DDD5' },
  photoBtnText:  { fontSize: 13, color: COLORS.primary, marginTop: 8, fontWeight: '600' },
  processingBox: { alignItems: 'center', padding: 32, backgroundColor: COLORS.white, borderRadius: RADIUS.lg, ...SHADOW.sm },
  processingText:{ fontSize: 15, fontWeight: '600', color: COLORS.text, marginTop: 16 },
  processingSubText: { fontSize: 12, color: COLORS.textMuted, marginTop: 4 },
  nextBtn:       { borderRadius: RADIUS.full, overflow: 'hidden', marginTop: 8 },
  nextGradient:  { paddingVertical: 18, flexDirection: 'row', alignItems: 'center', justifyContent: 'center' },
  nextText:      { fontSize: 16, fontWeight: '700', color: COLORS.white },
});
