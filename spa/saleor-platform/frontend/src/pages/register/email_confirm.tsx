import Link from "next/link";
import { useRouter } from "next/router";
import { useEffect, useMemo } from "react";
import { useAccountConfirmMutation } from "../../../generated/graphql"
import ErrorBlock from "../../components/blocks/ErrorBlock";
import Spinner from "../../components/Spinner";

export default function EmailConfirm() {
    const router = useRouter();
    const { email, token } = router.query
    
    const [emailConfirm, { loading, error }] = useAccountConfirmMutation();
    useMemo(() => {
        if(email && token)
            emailConfirm({
                variables: {
                    token: token as string, 
                    email: email as string
                }
            })
    }, [email, token])
    if (loading) return <Spinner />
    if (error) return <ErrorBlock />
    return (
        <div className="flex flex-col gap-4 place-items-center my-auto">
            <div className="text-3xl">Your email has been successfully confirmed!</div>
            <Link href={"/login"} replace className="text-sky-700 hover:underline underline-offset-2 py-2 px-5">Continue to login</Link>
        </div>
    )
}