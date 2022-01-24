import Head from 'next/head'
import Image from 'next/image'
import useSWR from 'swr'
import Link from 'next/link'
import { useRouter, Router } from 'next/router'

export default function Home() {
  const router = useRouter()
  const { username } = router.query

  console.log(username)

  const fetcher = (url) => fetch(url).then((res) => res.json())
  const { data, error } = useSWR(`http://localhost:8080/api/user/${username}`, fetcher)
  console.log(data)

  if (error) return <div>failed to load</div>
  if (!data) return <div>loading...</div>
  return (
    <div>
        {data.map(formtitle => (
            <Link href={`/user/${username}/${formtitle.slug}`}>
            <label><li>{formtitle.slug}</li></label>
            </Link>
        )
        )}
    </div>
  );
}