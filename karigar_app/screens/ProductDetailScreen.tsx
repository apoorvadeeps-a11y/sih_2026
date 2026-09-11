import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../constants/theme';
import { Product } from '../store/useAppStore';

const fallbackImage = 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&w=1000&q=85';

export default function ProductDetailScreen({ navigation, route }: any) {
  const product = route.params?.product as Product | undefined;
  const image = product?.image_url ?? fallbackImage;

  return (
    <View style={styles.screen}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.hero}>
          <Image source={{ uri: image }} style={styles.heroImage} />
          <TouchableOpacity style={styles.back} onPress={() => navigation.goBack()}><Ionicons name="chevron-back" size={24} color={COLORS.text} /></TouchableOpacity>
          <View style={styles.heroActions}><Ionicons name="heart-outline" size={22} color={COLORS.white} /><Ionicons name="share-social-outline" size={22} color={COLORS.white} /></View>
        </View>
        <View style={styles.body}>
          <View style={styles.liveRow}><View style={styles.liveBadge}><Ionicons name="checkmark-circle" size={13} color={COLORS.success} /><Text style={styles.liveText}>LIVE LISTING • सक्रिय</Text></View><Text style={styles.idText}>ID: #{product?.sku ?? '409-TK'}</Text></View>
          <Text style={styles.name}>{product?.title_hi ?? 'हाथ से बना टेराकोटा मटका (मिट्टी का पानी का घड़ा)'}</Text>
          <View style={styles.priceRow}><Text style={styles.price}>₹{product?.suggested_price ?? 850}</Text><Text style={styles.unit}>/ piece</Text><View style={styles.delivery}><Text style={styles.deliveryText}>Free local delivery</Text></View></View>
          <View style={styles.details}><Detail icon="cube-outline" label={`Category: ${product?.category ?? 'Home & Living'} • मिट्टी के बर्तन`} /><Detail icon="scan-outline" label="Dimensions: 14” height × 12” width (12L Capacity)" /><Detail icon="information-circle-outline" label="Made from pure organic river clay. Keeps water cool naturally." /></View>
          <View style={styles.divider} />
          <Text style={styles.sectionLabel}>ARTISAN'S INSIGHT • कारीगर का संदेश</Text>
          <View style={styles.audio}><View style={styles.play}><Ionicons name="play" size={16} color={COLORS.white} /></View><Text style={styles.wave}>▂▅▇▅▂▇▆▃▅▂▁▅▇▃▂</Text><Text style={styles.duration}>1:12</Text></View>
          <View style={styles.interested}><View style={styles.faces}><View style={styles.face}><Ionicons name="person" size={14} color="#7A513C" /></View><View style={styles.face}><Ionicons name="person" size={14} color="#7A513C" /></View><View style={styles.face}><Ionicons name="person" size={14} color="#7A513C" /></View></View><View><Text style={styles.interestedText}>3 Interested Buyers</Text><Text style={styles.activeText}>Active near Lucknow</Text></View></View>
          <TouchableOpacity style={styles.whatsapp} onPress={() => Alert.alert('Share listing', 'WhatsApp sharing is ready for this listing.')}><Ionicons name="logo-whatsapp" size={19} color={COLORS.white} /><Text style={styles.whatsappText}>Share to WhatsApp • ग्राहक को भेजें</Text></TouchableOpacity>
          <View style={styles.actions}><TouchableOpacity style={styles.edit}><Ionicons name="create-outline" size={16} color={COLORS.text} /><Text style={styles.actionText}>Edit • सुधारें</Text></TouchableOpacity><TouchableOpacity style={styles.sold} onPress={() => Alert.alert('Listing updated', 'This product was marked as sold.')}><Ionicons name="checkmark-circle-outline" size={16} color={COLORS.text} /><Text style={styles.actionText}>Mark as Sold</Text></TouchableOpacity></View>
        </View>
      </ScrollView>
    </View>
  );
}

function Detail({ icon, label }: { icon: any; label: string }) { return <View style={styles.detailRow}><Ionicons name={icon} size={18} color="#6A6A6A" /><Text style={styles.detailText}>{label}</Text></View>; }

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: '#F5F2EE' }, content: { paddingBottom: 24 }, hero: { height: 300, position: 'relative', backgroundColor: '#D8CEC5' }, heroImage: { width: '100%', height: '100%' }, back: { position: 'absolute', top: 48, left: 16, width: 38, height: 38, borderRadius: 19, backgroundColor: 'rgba(255,255,255,.9)', alignItems: 'center', justifyContent: 'center' }, heroActions: { position: 'absolute', top: 52, right: 18, flexDirection: 'row', gap: 14 }, body: { marginTop: -1, backgroundColor: '#FDFCFB', borderTopLeftRadius: 22, borderTopRightRadius: 22, padding: 16 }, liveRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }, liveBadge: { flexDirection: 'row', alignItems: 'center', gap: 4, borderWidth: 1, borderColor: '#87B997', backgroundColor: '#EDF8EF', borderRadius: 5, paddingHorizontal: 7, paddingVertical: 3 }, liveText: { fontSize: 10, color: '#39724D', fontWeight: '800' }, idText: { fontSize: 10, color: COLORS.textMuted, fontWeight: '700' }, name: { fontSize: 20, lineHeight: 25, fontWeight: '900', color: COLORS.text, marginTop: 12 }, priceRow: { marginTop: 14, backgroundColor: '#FBF3EB', borderRadius: 13, padding: 12, flexDirection: 'row', alignItems: 'baseline' }, price: { fontSize: 25, fontWeight: '900', color: COLORS.primary }, unit: { color: COLORS.textMuted, fontSize: 12, fontWeight: '700', marginLeft: 4 }, delivery: { marginLeft: 'auto', backgroundColor: '#FFF0D7', borderRadius: 10, paddingHorizontal: 8, paddingVertical: 5 }, deliveryText: { color: '#A0742C', fontSize: 10, fontWeight: '700' }, details: { marginTop: 12, gap: 9 }, detailRow: { flexDirection: 'row', alignItems: 'center', gap: 9 }, detailText: { flex: 1, color: COLORS.text, fontSize: 12, lineHeight: 16 }, divider: { height: 1, backgroundColor: '#E9E1DC', marginVertical: 15 }, sectionLabel: { color: '#757575', fontSize: 10, fontWeight: '800' }, audio: { height: 52, borderRadius: 13, backgroundColor: '#FBF3EB', marginTop: 8, flexDirection: 'row', alignItems: 'center', paddingHorizontal: 10, gap: 10 }, play: { width: 30, height: 30, borderRadius: 15, backgroundColor: '#6477AD', alignItems: 'center', justifyContent: 'center' }, wave: { color: '#6375A8', fontSize: 18, letterSpacing: 1, flex: 1 }, duration: { color: COLORS.textMuted, fontSize: 10, fontWeight: '700' }, interested: { borderWidth: 1, borderColor: '#EEE6E0', borderRadius: 13, marginTop: 14, padding: 10, flexDirection: 'row', alignItems: 'center', gap: 9 }, faces: { flexDirection: 'row', width: 56 }, face: { width: 28, height: 28, borderRadius: 14, backgroundColor: '#EAD6C5', alignItems: 'center', justifyContent: 'center', marginRight: -6, borderWidth: 2, borderColor: COLORS.white }, interestedText: { fontSize: 12, color: COLORS.text, fontWeight: '800' }, activeText: { fontSize: 10, color: COLORS.success, marginTop: 2 }, whatsapp: { marginTop: 12, height: 42, borderRadius: 22, backgroundColor: '#159B88', flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8 }, whatsappText: { color: COLORS.white, fontSize: 13, fontWeight: '800' }, actions: { flexDirection: 'row', gap: 8, marginTop: 9 }, edit: { flex: 1, height: 38, borderRadius: 20, borderWidth: 1, borderColor: '#E5DED8', flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 5 }, sold: { flex: 1, height: 38, borderRadius: 20, borderWidth: 1.5, borderColor: '#77716B', flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 5 }, actionText: { fontSize: 12, color: COLORS.text, fontWeight: '700' },
});