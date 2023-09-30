import Link from "next/link";
import { useContext, useState } from "react";
import { User } from "../../../generated/graphql";
import { CheckoutContext } from "../../contexts/checkoutContext";
import { useAppSelector } from "../../redux/hooks";
import { CheckoutInput } from "../checkout/CheckoutInput";

export default function ContactForm({ user, setEmail, email }: {user: User, setEmail, email}) {
    const {checkout} = useContext(CheckoutContext);
    const auth = useAppSelector((state) => state.auth);
    return (
        <div className="flex flex-col gap-3">
            <div className="flex flex-col sm:flex-row justify-between">
                <div className="text-xl self-start">Contact info</div>
                {!auth.loggedIn && <div className="text-sm self-start sm:self-center">do you already have an account? <Link href={{pathname: '/login', query: {save_checkout: true}}} className="text-sky-700">Register</Link></div>}
            </div>
            {auth.loggedIn ? (
                <div className="text-sm">
                    <div>{user?.firstName} {user?.lastName} {`(${user?.email})`}</div>
                    <Link href={{pathname: '/logout', query: {save_checkout: true}}} className="text-sky-700">Logout</Link>
                </div>
            ) : (
                <CheckoutInput data-testid="input-email" type="email" value={email} onChange={(e)=>setEmail(e.target.value)} className="grow" placeholder="E-Mail" />
            )}
            <div className="flex flex-row gap-3">
                <CheckoutCheckbox />
                <div className="align-center text-sm text-stone-500">
                    Receive news and offers via email
                </div>
            </div>
        </div>
    )
}

export function CheckoutCheckbox() {
    const [checked, setChecked] = useState(false);
    return (
        <>
            <input type="checkbox" onChange={() => setChecked(!checked)} className="self-center" />
        </>
    )
}