import Link from "next/link";

export default function  RegisterSuccess(){
    return(
        <div className="flex flex-col gap-4 place-items-center my-auto">
            <div className="text-3xl text-center font-semibold">Thank you for creating an account with us. You should receive an email confirmation link shortly!</div>
            <Link href={"/products"} className="hover:underline text-xl hover:underline-offset-2 text-sky-700">Continue shopping</Link>
        </div>
        
    )
}