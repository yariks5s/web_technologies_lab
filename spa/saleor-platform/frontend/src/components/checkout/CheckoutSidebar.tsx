import { useState } from "react";
import { Checkout, useAddPromoToCheckoutMutation } from "../../../generated/graphql";
import AuthAlert from "../Alert";
import SkyButton from "../buttons/SkyButton";
import { CheckoutInput } from "./CheckoutInput";
import CheckoutProductList from "./CheckoutProductList";
import CheckoutSummary from "./CheckoutSummary";



export default function CheckoutSidebar({ checkout, className="" } : {checkout: Checkout, className?: string}) {
  const [disabled, setDisabled] = useState(true);
  const [promoCode, setPromoCode] = useState("");
  const [showError, setShowError] = useState(false);
  const [addPromoToCheckout] = useAddPromoToCheckoutMutation()
  function onChange(value: string){
    if(value){
      setDisabled(false)
      setPromoCode(value)
    }
    else
      setDisabled(true)
  }
  function onClick(){
    addPromoToCheckout({
      variables: {
        id: checkout.id,
        promoCode: promoCode
      }
    }).then((data)=>{
      if(data.data.checkoutAddPromoCode.errors.length > 0)
        setShowError(true)
    })
  }
  return (
    <div className={`${className} grow py-10 px-5 divide-y divide-gray-400 bg-stone-200`}>
        <CheckoutProductList lines={checkout.lines} />
        <div className="flex flex-col">
          <AuthAlert show={showError} text={"Unfortunately the promo code is incorrect. Try it again"} hide={()=>setShowError(false)}/>
          <div className="flex md:flex-row flex-col justify-between gap-3 py-3">
            <CheckoutInput onChange={(e)=>onChange(e.target.value)} className={"border-gray-400 grow"} type={"text"} placeholder={"Discount code"} />
            <SkyButton onClick={onClick} disabled={disabled}>Apply</SkyButton>
          </div>
        </div>
        <CheckoutSummary discount={checkout.discount} shippingValue={checkout.shippingPrice?.gross?.amount} totalPrice={checkout.totalPrice} subtotalPrice={checkout.subtotalPrice}/>
    </div>
  )
}