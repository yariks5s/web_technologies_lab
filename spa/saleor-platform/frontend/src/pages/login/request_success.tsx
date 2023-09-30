import Link from "next/link";

export default function  RequestSuccess(){
    return(
        <div className="flex flex-col gap-4 place-items-center my-auto">
            <div className="text-3xl text-center font-semibold">Reset your password You should shortly receive an email with the link to reset your password!</div>
            <Link href={"/products"} className="hover:underline text-xl hover:underline-offset-2 text-sky-700">Continue shopping</Link>
        </div>
        
    )
}