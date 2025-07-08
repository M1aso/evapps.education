import { getDictionary, Locale } from "@/lib/dictionaries";

export default async function Page({ params }: { params: { locale: Locale } }) {
  const dict = await getDictionary(params.locale);
  return <div>{dict.profile}</div>;
}
