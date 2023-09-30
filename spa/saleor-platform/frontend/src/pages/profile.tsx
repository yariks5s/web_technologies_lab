import { useRouter } from "next/router"
import { useAppSelector } from "../redux/hooks"
import { GetUserQuery, useGetUserQuery } from "../../generated/graphql";
import Link from "next/link";
import Authorization from "../components/Authorization";
import ErrorBlock from "../components/blocks/ErrorBlock";
import Spinner from "../components/Spinner";
import ProfileLayout from "../components/layouts/ProfileLayout";
import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faChevronDown, faChevronUp } from "@fortawesome/free-solid-svg-icons";
import getFormattedDate from "../lib/getFormattedDate";
import { ApolloError } from "apollo-client";
import { AdressBlock } from "../components/adress/AdressBlock";
import Carousel from "../components/Carousel";


export default function Profile() {
  const auth = useAppSelector((state) => state.auth);
  const router = useRouter();
  const { data, loading, error } = useGetUserQuery();
  const [showOrders, setShowOrders] = useState(false);
  let component = <></>;
  if (loading) component = <Spinner />
  if (error) component = <ErrorBlock />
  if (auth.loggedIn) {
    component = (
      <ProfileLayout>
        <div>
          <ProfileHeader size="4xl">
            Account
          </ProfileHeader>
          <button className="text-gray-700 underline underline-offset-2" onClick={() => router.push("/logout")}>
            Log out
          </button>
        </div>
        <div className="flex flex-col gap-10 sm:flex-row sm:justify-between">
          <div className="flex flex-col gap-3 cursor-pointer" >
            <ProfileHeader size="3xl" onClick={() => setShowOrders(!showOrders)}>
              Order history
            </ProfileHeader>
            <Orders data={data} loading={loading} error={error} />
          </div>
          <div className="flex flex-col gap-4">
            <div className="flex flex-col gap-2">
              <ProfileHeader onClick={() => setShowOrders(!showOrders)} size="3xl">
                Account details
              </ProfileHeader>
              <div className="text-lg">
                {data?.me?.firstName} {data?.me?.lastName}
              </div>
              {data?.me?.addresses?.length > 0 ? (
                <div className="flex flex-col">
                  <div>Standart address: </div>
                  <div className="px-2">
                    <AdressBlock address={data?.me.addresses[0]} />
                  </div>
                </div>) : (<div className="text-stone-500">No address provided yet</div>)}
            </div>
            <Link href={'/adresses'} className="underline underline-offset-2 hover:decoration-2">Show addresses{data?.me?.addresses?.length > 0 ? `(${data.me?.addresses?.length})` : "(0)" }</Link>
          </div>
        </div>
      </ProfileLayout>
    )
  }
  return (
    <Authorization>
      {component}
    </Authorization>
  )
}

export function ProfileHeader({ size, children, onClick }: { size: "2xl" | "3xl" | "4xl", children, onClick?: () => void }) {
  return (
    <div className={`text-${size}`} onClick={onClick}>
      {children}
    </div>
  )
}

export function Orders({ data, loading, error }: { data: GetUserQuery, loading: boolean, error: ApolloError }) {
  if (error) return <ErrorBlock />
  if (loading) return <Spinner />
  if (data) {

    let component = data?.me?.orders?.edges?.length > 0 ? (
      <div className="flex flex-col gap-4">
        <Carousel nodes={data?.me?.orders?.edges}/>
      </div>
    ) : (
      <div className="text-gray-700">
        You haven't placed any orders yet.
      </div>
    )
    return <>{component}</>
  }
}

export function Order({ node }) {
  const [show, setShow] = useState(false);

  return (
    <div className="flex flex-col gap-2 px-2 py-4 rounded-lg">
      <div className="hover:underline hover:underline-offset-2 cursor-pointer" onClick={() => setShow(!show)}>
        View purchased products <FontAwesomeIcon icon={show ? faChevronUp : faChevronDown} />
      </div>
      {show && <ul>
        {node?.lines?.map((value) => (
          <li>
            <span>{value.productName}</span> x{value.quantity}
          </li>
        ))}
      </ul>}
      <div>
        Status: {node?.isPaid ? <span>Paid <FontAwesomeIcon icon={faCheck} color={"green"} /></span> : "Must be paid"}
      </div>
      <div>
        Completed: {getFormattedDate(node?.created)}
      </div>
    </div>
  )
}